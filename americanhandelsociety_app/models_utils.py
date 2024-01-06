from django.db import models


class BaseTextChoices(models.TextChoices):
    @classmethod
    def max_length(cls):
        return max((len(choice.value) for choice in cls))
