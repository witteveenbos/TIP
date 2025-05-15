from django.utils.translation import gettext_lazy as _
from wagtail.models import PageManager
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail_headless_preview.models import HeadlessPreviewMixin

from ..blocks.scenario_block import ScenarioBlock

from .base import BasePage


class HomePage(HeadlessPreviewMixin, BasePage):
    scenarios = StreamField(
        [
            ("scenario", ScenarioBlock()),
        ],
        verbose_name="Scenarios",
        blank=True,
        null=True,
        use_json_field=True,
    )

    content_panels = BasePage.content_panels + [
        FieldPanel("scenarios"),
    ]

    extra_panels = BasePage.extra_panels
    serializer_class = "main.pages.HomePageSerializer"

    objects: PageManager

    class Meta:
        verbose_name = _("Home")
