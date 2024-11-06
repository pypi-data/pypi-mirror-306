# Django
from django.db.models.expressions import F

# Standard Library
from datetime import date

# MuckRock
from muckrock.daily_active_users.models import DailyActiveUser


class DailyActiveUserMiddleware:
    """Middleware to log each user once per day"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """Ensure there is a single record for the active user for today's date"""

        if request.user.is_authenticated:
            organizations = list(
                request.user.organizations.values(
                    "id", "name", plan=F("entitlement__name")
                )
            )
            DailyActiveUser.objects.get_or_create(
                user=request.user,
                date=date.today(),
                defaults={"metadata": {"organizations": organizations}},
            )

        return self.get_response(request)
