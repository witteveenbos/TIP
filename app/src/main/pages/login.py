from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel
from wagtail.models import Page, PageManager
from wagtail_headless_preview.models import HeadlessPreviewMixin

from .base import BasePage


class LoginPage(HeadlessPreviewMixin, BasePage):
    title_label = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        help_text="title above the input fields, max 255 characters",
    )
    username_label = models.CharField(
        max_length=255,
        help_text="The placeholder and label text for the username input, max 255 characters",
    )

    password_label = models.CharField(
        max_length=255,
        help_text="The placeholder and label text for the password input, max 255 characters",
    )
    button_login_text = models.CharField(
        max_length=255,
        default="Login",
        help_text="The text for the login button, max 255 characters",
    )
    invalid_login = models.CharField(
        max_length=255,
        default="Invalid login",
        help_text="The text shown when the user enters wrong credentials",
    )
    redirect_page = models.ForeignKey(
        Page,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="The page to redirect to after successful login",
    )

    content_panels = BasePage.content_panels + [
        FieldPanel("title_label"),
        FieldPanel("username_label"),
        FieldPanel("password_label"),
        FieldPanel("button_login_text"),
        FieldPanel("invalid_login"),
        FieldPanel("redirect_page"),
    ]

    extra_panels = BasePage.extra_panels
    serializer_class = "main.pages.LoginPageSerializer"

    objects: PageManager

    show_in_menus_default = False
    subpage_types = []  # LoginPage cannot have any child pages

    class Meta:
        verbose_name = _("Login")
