from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import SimpleTestCase
from django.utils import timezone
from rest_framework.test import APIRequestFactory, force_authenticate

from main.models import WorkboardItems
from main.workboard_serializers import WorkboardItemsSerializer
from main.workboard_views import (
    WorkboardItemPositionUpdate,
    WorkboardItemsByPageList,
    WorkboardItemUpdate,
)


class WorkboardItemsSerializerTest(SimpleTestCase):
    def setUp(self):
        self.item = WorkboardItems(
            id=42,
            title="Original project title",
            description="Confidential description",
            organization="Owner",
            type="Zon",
            size_mw=12,
            status=4,
            acm_prio=3,
            secret=1,
            page_id=10,
            lane=2,
            sort_order=5,
            updated_at=timezone.now(),
        )
        self.factory = APIRequestFactory()

    def serialize(self, user):
        request = self.factory.get("/")
        request.user = user
        return WorkboardItemsSerializer(
            self.item, context={"request": request}
        ).data

    def assert_redacted(self, data):
        self.assertEqual(
            data,
            {
                "id": 42,
                "lane": 2,
                "title": "Vertrouwelijk project",
                "size_mw": 12,
                "organization": "Owner",
            },
        )

    def assert_full(self, data):
        self.assertEqual(set(data), set(WorkboardItemsSerializer.Meta.fields))
        self.assertEqual(data["title"], self.item.title)
        self.assertEqual(data["description"], self.item.description)
        self.assertEqual(data["type"], self.item.type)
        self.assertEqual(data["status"], self.item.status)
        self.assertEqual(data["secret"], self.item.secret)

    def test_confidential_item_is_redacted_for_anonymous_users(self):
        self.assert_redacted(self.serialize(AnonymousUser()))

    def test_confidential_item_is_redacted_for_other_organizations(self):
        user = get_user_model()(organization="Other")
        self.assert_redacted(self.serialize(user))

    def test_confidential_item_is_redacted_without_request_context(self):
        self.assert_redacted(WorkboardItemsSerializer(self.item).data)

    def test_confidential_item_is_visible_to_owning_organization(self):
        user = get_user_model()(organization="Owner")
        self.assert_full(self.serialize(user))

    def test_confidential_item_is_visible_to_staff_and_superusers(self):
        for flag in ("is_staff", "is_superuser"):
            with self.subTest(flag=flag):
                user = get_user_model()(organization="Other", **{flag: True})
                self.assert_full(self.serialize(user))

    def test_blank_organizations_do_not_grant_owner_access(self):
        self.item.organization = ""
        user = get_user_model()(organization="")
        data = self.serialize(user)
        self.assertEqual(data["title"], "Vertrouwelijk project")
        self.assertEqual(data["organization"], "")
        self.assertNotIn("description", data)

    def test_public_items_retain_all_fields(self):
        self.item.secret = 0
        self.assert_full(self.serialize(AnonymousUser()))

    def test_redaction_does_not_change_the_item(self):
        self.serialize(AnonymousUser())
        self.assertEqual(self.item.title, "Original project title")
        self.assertEqual(self.item.description, "Confidential description")

    def test_redaction_retains_zero_size(self):
        self.item.size_mw = 0
        self.assertEqual(self.serialize(AnonymousUser())["size_mw"], 0)

    def test_list_redacts_only_confidential_items(self):
        public_item = WorkboardItems(
            id=43, title="Public project", organization="Other", secret=0
        )
        data = WorkboardItemsSerializer([self.item, public_item], many=True).data
        self.assert_redacted(data[0])
        self.assertEqual(data[1]["title"], "Public project")
        self.assertEqual(set(data[1]), set(WorkboardItemsSerializer.Meta.fields))

    def test_list_response_uses_request_permissions(self):
        for user, full in (
            (AnonymousUser(), False),
            (get_user_model()(organization="Other"), False),
            (get_user_model()(organization="Owner"), True),
            (get_user_model()(is_staff=True), True),
        ):
            with self.subTest(user=user, full=full):
                request = self.factory.get("/")
                force_authenticate(request, user=user)
                with patch.object(
                    WorkboardItemsByPageList, "get_queryset", return_value=[self.item]
                ):
                    response = WorkboardItemsByPageList.as_view()(request, page_id=10)
                self.assertEqual(response.status_code, 200)
                if full:
                    self.assert_full(response.data[0])
                else:
                    self.assert_redacted(response.data[0])

    def test_update_response_retains_details_for_owner_and_admin(self):
        for user in (
            get_user_model()(id=1, organization="Owner"),
            get_user_model()(id=2, organization="Other", is_staff=True),
        ):
            with self.subTest(user=user):
                request = self.factory.patch(
                    "/", {"title": self.item.title}, format="json"
                )
                force_authenticate(request, user=user)
                with (
                    patch.object(WorkboardItemUpdate, "get_object", return_value=self.item),
                    patch.object(WorkboardItemUpdate, "can_edit", return_value=True),
                    patch.object(WorkboardItems, "save"),
                ):
                    response = WorkboardItemUpdate.as_view()(request, pk=self.item.pk)
                self.assertEqual(response.status_code, 200)
                self.assert_full(response.data)

    def test_position_response_retains_details_for_owner_and_admin(self):
        for user in (
            get_user_model()(id=1, organization="Owner"),
            get_user_model()(id=2, organization="Other", is_staff=True),
        ):
            with self.subTest(user=user):
                request = self.factory.patch("/", {"lane": 2}, format="json")
                force_authenticate(request, user=user)
                with (
                    patch.object(
                        WorkboardItemPositionUpdate, "get_object", return_value=self.item
                    ),
                    patch("main.workboard_views.WorkboardPage.objects.get") as get_page,
                    patch("main.workboard_views.transaction.atomic"),
                    patch.object(WorkboardItems.objects, "select_for_update") as locked,
                    patch.object(WorkboardItems.objects, "bulk_update"),
                    patch("main.workboard_views.WorkboardItemModification.objects.create"),
                ):
                    get_page.return_value.phase = "inzicht & invoeren"
                    locked.return_value.get.return_value = self.item
                    locked.return_value.filter.return_value.order_by.return_value = [
                        self.item
                    ]
                    response = WorkboardItemPositionUpdate.as_view()(
                        request, pk=self.item.pk
                    )
                self.assertEqual(response.status_code, 200)
                self.assert_full(response.data)
