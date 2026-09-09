from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.models import Orderable, PageManager
from wagtail_headless_preview.models import HeadlessPreviewMixin

from .base import BasePage


class SwimmingLane(Orderable):
    workboard = ParentalKey(
        "main.WorkboardPage",
        on_delete=models.CASCADE,
        related_name="swimming_lanes",
    )
    label = models.CharField(max_length=255)
    minimum_energy = models.FloatField()
    maximum_energy = models.FloatField()
    minimum_risk = models.FloatField()
    maximum_risk = models.FloatField()

    panels = [
        FieldPanel("label"),
        FieldPanel("minimum_energy"),
        FieldPanel("maximum_energy"),
        FieldPanel("minimum_risk"),
        FieldPanel("maximum_risk"),
    ]


class WorkboardPage(HeadlessPreviewMixin, BasePage):
    PHASE_CHOICES = [
        ("inzicht & invoeren", _("inzicht & invoeren")),
        ("Samenwerksessie", _("Samenwerksessie")),
        ("Versies vergelijken", _("Versies vergelijken")),
        ("integraal programmeren", _("integraal programmeren")),
    ]

    phase = models.CharField(max_length=32, choices=PHASE_CHOICES)

    parent_page_types = ["main.HomePage"]

    content_panels = BasePage.content_panels + [
        FieldPanel("phase"),
        InlinePanel("swimming_lanes", label=_("Swimming lanes")),
    ]

    extra_panels = BasePage.extra_panels
    serializer_class = "main.pages.WorkboardPageSerializer"

    objects: PageManager

    class Meta:
        verbose_name = _("Workboard")