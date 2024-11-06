# Django
from django.contrib import admin
from django.http.response import HttpResponse
from django.utils.safestring import mark_safe

# Standard Library
import csv
import json
from itertools import chain

# MuckRock
from muckrock.daily_active_users.models import DailyActiveUser


@admin.register(DailyActiveUser)
class DailyActiveUserAdmin(admin.ModelAdmin):
    """Daily Active User admin"""

    date_hierarchy = "date"
    list_display = ("user", "date")
    list_select_Related = ("user",)
    readonly_fields = ("user", "date", "formatted_metadata")
    fields = ("user", "date", "formatted_metadata")
    actions = ["export_as_csv"]

    def formatted_metadata(self, obj):
        json_data = json.dumps(obj.metadata, indent=4)
        return mark_safe(f"<pre>{json_data}</pre>")

    formatted_metadata.short_description = "Metadata"

    def export_as_csv(self, request, queryset):
        """Export daily active users"""

        meta = self.model._meta
        field_names = [
            "user",
            "date",
        ]

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f"attachment; filename={meta}.csv"
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow(
                [getattr(obj, field) for field in field_names]
                + list(
                    chain(
                        *[[m["name"], m["plan"]] for m in obj.metadata["organizations"]]
                    )
                )
            )

        return response

    export_as_csv.short_description = "Export Selected"
