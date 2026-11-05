from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + \
        (("Organization", {"fields": ("organization",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Organization", {"fields": ("organization",)}),
    )


admin.site.register(User, CustomUserAdmin)
