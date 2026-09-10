from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet

from .pages import *  # NOQA: F403


@register_snippet
class WorkboardItems(models.Model):
    TYPE_CHOICES = [
        ("Woningbouw", "Woningbouw"),
        ("Laadinfra", "Laadinfra"),
        ("Bedrijventerrein / logistiek", "Bedrijventerrein / logistiek"),
        ("Zon", "Zon"),
    ]
    STATUS_CHOICES = [
        (1, "Idee (Zacht)"),
        (2, "Beleidsvoornemen (Zacht)"),
        (3, "Planvorming (Zacht)"),
        (4, "Besluitvorming loopt (Vast)"),
        (5, "Vastgesteld / in uitvoering (Vast)"),
    ]
    ACM_PRIO_CHOICES = [
        (0, "Geen prio"),
        (1, "Categorie 1: Congestieverzachters"),
        (2, "Categorie 2: Veiligheid"),
        (3, "Categorie 3: Basisbehoeften"),
    ]

    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    organization = models.CharField(max_length=255, blank=True)
    type = models.CharField(
        max_length=32, choices=TYPE_CHOICES, default="Woningbouw")
    size_mw = models.IntegerField("Size (MW)", default=0)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    acm_prio = models.IntegerField(
        choices=ACM_PRIO_CHOICES, default=0, verbose_name="ACM prioriteringskader")
    page_id = models.IntegerField(null=True, blank=True)
    lane = models.IntegerField(default=0)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="updated_workboard_items",
    )
    updated_at = models.DateTimeField(auto_now=True)

    panels = [
        FieldPanel("title"),
        FieldPanel("description"),
        FieldPanel("organization"),
        FieldPanel("type"),
        FieldPanel("size_mw"),
        FieldPanel("status"),
        FieldPanel("acm_prio"),
        FieldPanel("page_id"),
        FieldPanel("lane"),
        FieldPanel("updated_by"),
    ]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Workboard item")
        verbose_name_plural = _("Workboard items")


class WorkboardItemModification(models.Model):
    item = models.ForeignKey(
        WorkboardItems,
        on_delete=models.CASCADE,
        related_name="modifications",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="workboard_item_modifications",
    )
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-updated_at"]
