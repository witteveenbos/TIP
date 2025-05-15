from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.fields import RichTextField
from wagtail.images import get_image_model_string


@register_setting
class SiteSetting(BaseSiteSetting):
    logo = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Logo"),
        help_text=_("Brand logo used in the navbar and throughout the site."),
    )
    favicon = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="favicon",
        verbose_name=_("Favicon"),
    )
    gtm_id = models.CharField(max_length=50, blank=True)
    google_site_verification = models.CharField(max_length=255, blank=True)

    cookie_content = RichTextField(
        blank=True, null=True, verbose_name=_("Cookie bar content"), features=[]
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("logo"),
                FieldPanel("favicon"),
            ],
            heading=_("Branding"),
        ),
        FieldPanel("gtm_id"),
        FieldPanel("cookie_content"),
    ]

    def __str__(self):
        return str(self.site)

    class Meta:
        verbose_name = _("Site setting")
        verbose_name_plural = _("Site settings")
