# americanhandelsociety-members

# Get Started: Dockerize Database and App

```bash
docker compose up
```

# (Alternate) Get Started: Dockerize Database, but not App

**1. Standup containerized version of Postgres.**

```bash
docker compose up postgres
```

**2. Setup Environment.**

```bash
cp .env.example .env
```

**3. Run migrations.**

```bash
# in another terminal window
pipenv run python manage.py migrate
```

**4. Run the app.**

```bash
# in the terminal window where you ran migrations
pipenv run python manage.py runserver
```

**4. (for dev purposes) Install pre-commit.** This repo comes with a pre-commit-config.yaml file, which includes some basic formatting hooks (e.g., a trailing whitespace fixer, the python auto-formatter black, etc.). These hooks execute before every commit, so the codebase stays clean, beautiful, and functional, without much effort.

```bash
pipenv run pre-commit install
```

# Tests

Run the tests like so:

```bash
pipenv run pytest
```

You also can run the tests with different options, depending on your needs:

```bash
# Print all logger output to terminal
pipenv run pytest --log-cli-level=INFO

# Do not stop the Postgres database container after running tests
DO_NOT_KILL_DB=true pipenv run pytest
```
