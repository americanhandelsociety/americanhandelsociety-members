import json
import logging
import os
from time import sleep

import docker
import pytest
from string import ascii_lowercase
from random import sample
from datetime import datetime
from dateutil.relativedelta import relativedelta

from americanhandelsociety_app.models import Member, Address


DO_NOT_KILL_DB = os.getenv("DO_NOT_KILL_DB", False)
os.environ["APP_ENV"] = "TESTING"


class PostgreSQLContainer:
    """A PostgreSQL Container Object.

    This class provides a mechanism for managing PostgreSQL Docker
    containers so that a database can be injected into tests. Class
    Attributes:     config (object): A Configuration Factory object.
    container (object): The Docker container object.     docker_client
    (object): Docker client.     db_environment (list): Database
    environment configuration variables.     db_ports (dict): Dictionary
    of database port mappings.
    """

    def __init__(self):
        self.container = None
        self.container_name = "postgres_test"
        self.docker_client = docker.from_env()
        self.db_environment = [
            "POSTGRES_USER={}".format("ahs_admin"),
            "POSTGRES_PASSWORD={}".format("gfhandel"),
            "POSTGRES_DB={}".format("american_handel_society"),
        ]
        self.db_ports = {"5432/tcp": 5433}
        self.image_name = "postgres"
        self.image_version = "12"

    def get_postgresql_image(self):
        """Output the PostgreSQL image from the configuration.

        Returns:
            str: The PostgreSQL image name and version tag.
        """
        return "{}:{}".format(self.image_name, self.image_version)

    def start_container(self):
        """Start PostgreSQL Container."""
        if DO_NOT_KILL_DB and self.get_db_if_running():
            return

        if self.get_db_if_running():
            return

        try:
            self.docker_client.images.pull(self.get_postgresql_image())
        except Exception:
            logging.error("Failed to pull postgres image")
            raise RuntimeError

        self.container = self.docker_client.containers.run(
            self.get_postgresql_image(),
            detach=True,
            auto_remove=True,
            name=self.container_name,
            environment=self.db_environment,
            ports=self.db_ports,
        )
        sleep(2)

        logging.info("PostgreSQL container running!")

    def stop_if_running(self):
        if DO_NOT_KILL_DB:
            return

        try:
            running = self.docker_client.containers.get(self.container_name)
            logging.info(f"Killing running container '{self.container_name}'")
            running.stop()
        except Exception as e:
            if "404 Client Error: Not Found" in str(e):
                return
            raise e

    def get_db_if_running(self):
        """Return the container or None."""
        try:
            return self.docker_client.containers.get(self.container_name)
        except Exception as e:
            if "404 Client Error: Not Found" in str(e):
                return


@pytest.fixture(scope="session")
def django_db_setup(
    request,
    django_test_environment,
    django_db_blocker,
    django_db_use_migrations,
    django_db_keepdb,
    django_db_createdb,
    django_db_modify_db_settings,
):
    """Top level fixture to ensure test databases are available."""
    from django.test.utils import setup_databases, teardown_databases

    setup_databases_args = {}

    if not django_db_use_migrations:
        _disable_native_migrations()

    if django_db_keepdb and not django_db_createdb:
        setup_databases_args["keepdb"] = True

    with django_db_blocker.unblock():
        # Custom: Start postgres container
        postgres = PostgreSQLContainer()
        postgres.start_container()

        db_cfg = setup_databases(
            verbosity=request.config.option.verbose,
            interactive=False,
            **setup_databases_args,
        )

    def teardown_database():
        with django_db_blocker.unblock():
            try:
                teardown_databases(db_cfg, verbosity=request.config.option.verbose)

                # Custom: Stop postgres container
                postgres.stop_if_running()
            except Exception as exc:
                request.node.warn(
                    pytest.PytestWarning(
                        "Error when trying to teardown test databases: %r" % exc
                    )
                )

    if not django_db_keepdb:
        request.addfinalizer(teardown_database)


@pytest.fixture
def address():
    address_data = {
        "street_address": "The Handel House Trust Ltd",
        "street_address_2": "25 Brook Street",
        "city": "London",
        "zip_postal_code": "W1K 4HB",
        "country": "UK",
    }

    address = Address.objects.create(**address_data)

    return address


@pytest.fixture
def member(address):
    data = {
        "email": "rodelinda@lombardy.sa",
        "password": "cuzzoni",
        "first_name": "Queen",
        "last_name": "Rodelinda",
        "available_in_directory": True,
        "membership_type": "REGULAR",
        "contact_preference": "EMAIL",
        "phone_number": "44 20 7495 1685",
        "institution": "Handel House Foundation of America",
        "address": address,
    }

    member = Member.objects.create(**data)

    return member


@pytest.fixture
def member_not_in_directory():
    data = {
        "email": "gismonda@rome.sa",
        "password": "durastanti",
        "first_name": "Lady",
        "last_name": "Gismonda",
        "available_in_directory": False,
        "membership_type": "REGULAR",
        "contact_preference": "EMAIL",
        "phone_number": "44 20 7495 1685",
        "institution": "Handel House Foundation of America",
    }

    member = Member.objects.create(**data)

    return member


def generate_random_string(length=8):
    return "".join(sample(ascii_lowercase, length))


def modify_field_config(model, field_name, auto_now_setting):
    field = model._meta.get_field(field_name)
    field.auto_now = auto_now_setting


@pytest.fixture
def artificially_backdated_pre_004_migration_members():
    modify_field_config(Member, "last_updated", False)
    members_list = [
        Member.objects.create(
            email=f"{generate_random_string()}@email.com",
            password=generate_random_string(),
            first_name=generate_random_string(length=5).upper(),
            last_name=generate_random_string().upper(),
            date_joined=datetime.utcnow() + relativedelta(years=-1 * x),
        )
        for x in range(1, 4)
    ]
    modify_field_config(Member, "last_updated", True)
    return members_list
