from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel
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
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("minimum_energy"),
                        FieldPanel("maximum_energy"),
                        FieldPanel("minimum_risk"),
                        FieldPanel("maximum_risk"),
                    ],
                ),
            ]
        ),
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
        MultiFieldPanel(
            [
                FieldRowPanel([FieldPanel("phase")]),
            ],
            "Workboard phase",
            help_text=(
                "In a workboard, users and organizations work together to plan "
                "projects. To set up a workboard, do the following: "
                "1. In Settings > Groups, add a new user group. "
                "2. Fill in the form below and add lanes. "
                "3. Set this workboard's access to the new group. "
                "4. Create users in Settings > Users and add them to an organization and the new user group."
            ),
        ),
        InlinePanel("swimming_lanes", label=_("Swimming lanes")),
    ]

    extra_panels = BasePage.extra_panels
    serializer_class = "main.pages.WorkboardPageSerializer"

    objects: PageManager

    class Meta:
        verbose_name = _("Workboard")
