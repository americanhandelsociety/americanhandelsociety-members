import json
import requests

from django.conf import settings

# Reference: https://www.rootstrap.com/blog/real-time-monitoring-using-django-and-slack-webhooks-2/
def _send(payload):
    requests.request(
        method="POST",
        url=settings.SLACK_ALERTS_URL,
        data=payload,
        headers={"content-type": "application/json"},
    )


def message_non_error(message):
    data = {
        "text": f"INFO Message!",
        "attachments": [
            {
                "color": "#70a839",
                "fields": [
                    {"title": "Message", "value": f"```{message}```"},
                ],
            }
        ],
    }
    _send(payload=json.dumps(data))


def message_error(message, function, alert_everyone=True):
    data = {
        "text": "<!here> ERROR message!" if alert_everyone else "ERROR message!",
        "attachments": [
            {
                "color": "#ba3232",
                "fields": [
                    {"title": "Function:", "value": function},
                    {
                        "title": "Details:",
                        "value": message,
                    },
                ],
            }
        ],
    }
    _send(payload=json.dumps(data))
