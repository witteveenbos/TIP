from urllib.parse import unquote

from django.urls import reverse
from wagtail.models import BaseViewRestriction, Site
from wagtail.test.utils import WagtailPageTests

from main.factories.base_page import BasePageFactory
from main.pages.login import LoginPage
from nextjs.factories import PageViewRestrictionFactory


class PasswordProtectedPageApiTest(WagtailPageTests):
    def setUp(self):
        self.site = Site.objects.first()

        self.root_page = BasePageFactory.create(title="Start", parent=None)
        self.site.root_page = self.root_page
        self.site.save()

    def test_redirect_page_if_user_is_not_logged_in(self):
        sub_page = BasePageFactory.create(title="Child page", parent=self.root_page)
        PageViewRestrictionFactory.create(
            page=sub_page,
            restriction_type=BaseViewRestriction.LOGIN,
        )

        url = reverse("nextjs:page_by_path:listing")
        response = self.client.get(
            f"{url}?html_path=/child-page",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue("redirect" in data)
        
    def test_redirect_to_login_page_with_next_parameter(self):
        # Create a LoginPage
        login_page = LoginPage(
            title="Login",
            slug="login",
            title_label="Log in",
            username_label="Username",
            password_label="Password",
            button_login_text="Login",
            invalid_login="Invalid credentials",
        )
        self.root_page.add_child(instance=login_page)
        login_page.save_revision().publish()

        # Create a protected page
        sub_page = BasePageFactory.create(title="Protected page", parent=self.root_page)
        PageViewRestrictionFactory.create(
            page=sub_page,
            restriction_type=BaseViewRestriction.LOGIN,
        )

        url = reverse("nextjs:page_by_path:listing")
        response = self.client.get(
            f"{url}?html_path=/protected-page",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue("redirect" in data)

        # Verify it redirects to the LoginPage with next parameter
        redirect_destination = data["redirect"]["destination"]
        self.assertIn("/login", redirect_destination)
        self.assertIn("next=", redirect_destination)
        # Decode the URL to check for the protected page path
        decoded_destination = unquote(redirect_destination)
        self.assertIn("/protected-page", decoded_destination)

    def test_proper_page_if_user_is_logged_in(self):
        self.login()

        sub_page = BasePageFactory.create(title="Child page", parent=self.root_page)
        PageViewRestrictionFactory.create(
            page=sub_page,
            restriction_type=BaseViewRestriction.LOGIN,
        )

        url = reverse("nextjs:page_by_path:listing")
        response = self.client.get(
            f"{url}?html_path=/child-page",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["component_name"], "BasePage")
