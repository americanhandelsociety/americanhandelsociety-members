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
