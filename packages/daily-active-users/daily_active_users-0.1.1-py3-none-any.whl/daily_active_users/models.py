from datetime import date

from django.conf import settings
from django.db import models


class DailyActiveUser(models.Model):
    """A log of user activity per day"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="+",
    )
    date = models.DateField(default=date.today)
    metadata = models.JSONField(default=dict)

    class Meta:
        unique_together = [("user", "date")]
