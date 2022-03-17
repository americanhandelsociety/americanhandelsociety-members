# The Official Website of the American Handel Society
The American Handel Society (AHS), an established 501(c)3 non-profit, seeks to foster study of the life, works, and times of the composer George Frideric Handel (1685-1759) and to encourage and support the performance of his music.

This repo contains the code for the AHS website – a Django project with the following features:

* a user flow for joining the Society (made possible, in part, by a Paypal integration)
* secure user login and protected, members-only views
* a Django admin dashboard for member management
* interactive data tables for newsletters, awards, and people
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

# Deployments
This project uses Heroku as its deployment and platform service. Our Heroku project has three main components:

1. "Review Apps": a complete, but short-lived version of the AHS website with a unique URL; Heroku **automatically** stands up a review app when an engineer pushes code to a branch of this repo.
2. "Staging" pipeline: a production-like version of the AHS website available at https://americanhandelsociety-staging.herokuapp.com/; Heroku **automatically** deploys to staging when an engineer merges a branch into `main` or pushes to `main`.
3. "Production" pipeline: the production version of the AHS website available at https://www.americanhandelsociety.org/; only authenticated Heroku users can deploy to production – they do so using the Heroku CLI.

Thank you to our friends at DataMade for [the lovely guide on Django and Heroku](https://github.com/datamade/how-to/tree/main/deployment/heroku).

# Logging

This project uses the Django logging system. Logs reside in two locations:

**ONE.** Heroku. Heroku makes available the log output of the app itself; however, Heroku only stores the last 1,500 lines, and they expire after one week.

```bash
# using the Heroku CLI
heroku logs --app americanhandelsociety-staging
heroku logs --app americanhandelsociety-staging --tail

heroku logs --app americanhandelsociety
heroku logs --app americanhandelsociety --tail
```

**TWO.** Slack. The American Handel Society has a Slack workspace with two channels: `#site-logs-staging` and `#site-logs-production`. Each channel hooks into a custom Slack "Incoming Webhook" (called `django-logger`) – or, in other words, each channel connects to a Webhook URL, which accepts POST requests that Slack renders as messages.

The AHS Django project only logs critical user-flow events to the Slack channels (made possible by a `logging.Handler` custom class). These events include: a user completes the `Join` form, a user cancels the `Join` flow, and a user submits payment (with success or error).

Reference: https://www.rootstrap.com/blog/real-time-monitoring-using-django-and-slack-webhooks-2/
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
# Emails

This project sets SMTP values in the settings in order to enable password reset via e-mail.
Those settings are largely hardcoded, except for e-mail and passsword. These two values read environment
 variables. Here's a partial copy from `americanhandelsociety/settings.py`:

```python
EMAIL_HOST_USER = os.environ.get("AHS_EMAIL")
EMAIL_HOST_PASSWORD = os.environ.get("AHS_EMAIL_PW")
```

These two values need to be set in your local environment for password reset to work in local development.

You can set them this way:

```bash
export AHS_EMAIL=ahs.example@gmail.org
export AHS_EMAIL_PW=super_secure_password
```

Production values are set in Heroku, and need not necessarily be exactly duplicated for local functionality.
The settings file currently defaults to using gmail as a SMTP server, and it is assumed that whatever values
you use locally are also gmail values.
