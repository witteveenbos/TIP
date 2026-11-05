from typing import List

from rest_framework import serializers
from wagtail import fields
from wagtail.admin.templatetags.wagtailuserbar import wagtailuserbar
from wagtail.api.v2 import serializers as wagtail_serializers

from sitesettings.models import SiteSetting
from sitesettings.serializers import SiteSettingSerializer
from ..serializers import SeoSerializer
from . import BasePage


class BasePageSerializer(serializers.ModelSerializer):
    serializer_field_mapping = (
        serializers.ModelSerializer.serializer_field_mapping.copy()
    )
    serializer_field_mapping.update(
        {fields.StreamField: wagtail_serializers.StreamField}
    )

    seo = serializers.SerializerMethodField()
    site_setting = serializers.SerializerMethodField()
    wagtail_userbar = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    organization = serializers.SerializerMethodField()

    class Meta:
        model = BasePage
        fields: List[str] = [
            "title",
            "last_published_at",
            "seo_title",
            "search_description",
            "seo",
            "site_setting",
            "wagtail_userbar",
            "username",
            "organization",
        ]

    def get_seo(self, page):
        return SeoSerializer(page).data

    def get_site_setting(self, page):
        site_setting = SiteSetting.for_site(page.get_site())
        return SiteSettingSerializer(site_setting).data

    def get_wagtail_userbar(self, page):
        request = self.context.get("request", None)
        if not request:
            return None

        in_preview_panel = getattr(request, "in_preview_panel", False)
        if in_preview_panel:
            return None

        if not hasattr(request, "user"):
            return None

        html = wagtailuserbar({"request": request, "self": page})

        if not html:
            return None

        return {
            "html": html,
        }

    def get_username(self, page):
        """
        Retrieve the username of the authenticated user from the request context.

        This method extracts the request object from the serializer's context and
        returns the username of the authenticated user if available.

        Args:
            page: The page object being serialized (unused in this method).

        Returns:
            str or None: The username of the authenticated user if the request exists
                         and the user is authenticated, otherwise None.

        Note:
            This method is compatible with Wagtail 6.x/7.x and Django 4.2/5.x, as it
            uses standard Django authentication patterns that remain consistent across
            these versions.
        """
        request = self.context.get("request", None)

        if request and request.user.is_authenticated:
            try:
                return request.user.get_username()
            except Exception as e:
                import logging

                logger = logging.getLogger(__name__)
                logger.error(
                    f"Error getting username for user {request.user.id}: {e}")
                return None
        return None

    def get_organization(self, page):
        request = self.context.get("request", None)

        if request and request.user.is_authenticated:
            try:
                org = getattr(request.user, "organization", None)
                if callable(org):
                    org = org()
                elif org is None and hasattr(request.user, "get_organization"):
                    org = request.user.get_organization()
                if org is not None:
                    return getattr(org, "name", str(org))
                return None
            except Exception as e:
                import logging

                logger = logging.getLogger(__name__)
                logger.error(
                    f"Error getting organization for user {request.user.id}: {e}"
                )
                return None
        return None
