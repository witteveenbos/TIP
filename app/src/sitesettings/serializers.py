from rest_framework import serializers
from rest_framework.fields import Field

from sitesettings.models import SiteSetting
from customimage.serializers import CustomImageSerializer


class ImageSerializedField(Field):
    """A custom serializer used in Wagtails v2 API."""

    def to_representation(self, value):
        """Return the image URL, title and dimensions."""
        return {
            "url": value.file.url,
            "title": value.title,
            "width": value.width,
            "height": value.height,
        }


class SiteSettingSerializer(serializers.ModelSerializer):
    logo = ImageSerializedField()
    favicon = ImageSerializedField()

    class Meta:
        model = SiteSetting
        fields = [
            "gtm_id",
            "cookie_content",
            "logo",
            "favicon",
        ]
