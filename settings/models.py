from django.db import models


class SiteSettings(models.Model):
    logo = models.BinaryField(null=True, editable=True)
    searchable_table = models.BooleanField(default=False)

    # Other fields...

    def __str__(self):
        return "Site Settings"
