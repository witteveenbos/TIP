from django.db import models
from energy.models import ProvinceIDs, RegionIDs


class FutureVision(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    author = models.CharField(max_length=255)
    scenario = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    json_data = models.JSONField()
    geo_id = models.CharField(
        choices=[*ProvinceIDs.choices, *RegionIDs.choices], max_length=255
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_geo_id_display(self):
        return dict(ProvinceIDs.choices + RegionIDs.choices).get(self.geo_id, None)

    class Meta:
        ordering = ["updated_at"]
