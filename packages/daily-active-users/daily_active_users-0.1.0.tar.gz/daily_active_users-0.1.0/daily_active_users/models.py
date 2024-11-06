# Django
from django.db import models

# Standard Library
from datetime import date


class DailyActiveUser(models.Model):
    """A log of user activity per day"""

    user = models.ForeignKey(
        "auth.User",
        on_delete=models.PROTECT,
        related_name="+",
    )
    date = models.DateField(default=date.today)
    metadata = models.JSONField(default=dict)

    class Meta:
        unique_together = [("user", "date")]
