from django.test import Client, SimpleTestCase


class CsrfTokenViewTest(SimpleTestCase):
    def test_csrf_endpoint_returns_token_and_sets_cookie(self):
        response = self.client.get("/wt/api/nextjs/v1/csrf/")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["csrf_token"])
        self.assertIn("csrftoken", response.cookies)


class LoginViewCsrfTest(SimpleTestCase):
    def test_login_rejects_post_without_csrf_token(self):
        client = Client(enforce_csrf_checks=True)
        response = client.post(
            "/wt/api/nextjs/v1/login/",
            {"username": "user", "password": "invalid"},
        )

        self.assertEqual(response.status_code, 403)
