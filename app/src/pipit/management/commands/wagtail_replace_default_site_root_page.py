from django.core.management.base import BaseCommand
from wagtail.models import Site, Page
from main.models import LoginPage, HomePage


class Command(BaseCommand):
    """
    Switch site root page to HomePage

    Example:
        manage.py wagtail_replace_default_site_root_page
    """

    def handle(self, *args, **options):
        from sitesettings.models import SiteSetting

        if Site.objects.count() > 1:
            return

        if Page.objects.count() > 2:
            return

        site = Site.objects.first()

        if not site:
            return

        if site.root_page.specific.__class__.__name__ != Page.__name__:
            return

        root_page = Page.objects.filter(depth=1).first()

        new_site_page = HomePage(title="Home Page", slug="home-page")
        root_page.add_child(instance=new_site_page)

        old_site_page = site.root_page
        site.root_page = new_site_page
        site.save()

        old_site_page.delete()

        
        # Refresh the page instance to ensure it has the proper ID and database state
        new_site_page.refresh_from_db()

        # Create a login page as a child of the home page
        login_page = LoginPage(
            title="Login",
            slug="login",
            title_label="Log in",
            username_label="Username",
            password_label="Password",
            button_login_text="Login",
            invalid_login="Invalid username or password",
            redirect_page=new_site_page,
        )
        new_site_page.add_child(instance=login_page)
        login_page.save_revision().publish()

        # Create site settings if they don't exist
        SiteSetting.objects.get_or_create(site=site)

        self.stdout.write("Default site root page was changed")
        self.stdout.write("Login page was created")
        self.stdout.write("Site settings initialized")
