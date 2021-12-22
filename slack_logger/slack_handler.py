import logging

from django.conf import settings

from slack_logger.slack_interface import message_error, message_non_error


class SlackHandler(logging.Handler):
    def emit(self, record):
        if not settings.SLACK_ALERTS_URL:
            return None

        if record.levelno == logging.ERROR:
            message_error(record.message, record.funcName)
        else:
            message_non_error(record.message)
