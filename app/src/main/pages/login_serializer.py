from rest_framework import serializers

from . import LoginPage
from .base_serializer import BasePageSerializer


class LoginPageSerializer(BasePageSerializer):
    redirect_page_url = serializers.SerializerMethodField()

    def get_redirect_page_url(self, obj):
        if obj.redirect_page:
            return obj.redirect_page.url
        return None

    class Meta:
        model = LoginPage
        fields = [
            "title_label",
            "username_label",
            "password_label",
            "button_login_text",
            "invalid_login",
            "redirect_page_url",
        ] + BasePageSerializer.Meta.fields
