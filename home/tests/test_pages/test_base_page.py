from unittest.mock import MagicMock

import pytest
from django.http import HttpRequest
from home.models.pages.base_page import BasePage, get_superuser


class TestGetSuperuser:
    def test_returns_superuser(self, admin_user):
        assert get_superuser() == admin_user

    def test_returns_none_when_no_superuser(self, db):
        assert get_superuser() is None

    def test_returns_first_superuser(self, db):
        from django.contrib.auth import get_user_model

        User = get_user_model()
        user1 = User.objects.create_superuser(username="su1", password="pw", email="su1@t.com")
        user2 = User.objects.create_superuser(username="su2", password="pw", email="su2@t.com")
        assert get_superuser() == user1
        assert get_superuser() != user2


class TestBasePageClean:
    def test_clean_passes_when_not_in_menu(self, db, admin_user, wagtail_image):
        page = BasePage(title="Test", user=admin_user, avatar=wagtail_image)
        page.show_in_menus = False
        page.menu_icon = ""
        page.clean()

    def test_clean_raises_when_in_menu_no_icon(self, db, admin_user, wagtail_image):
        page = BasePage(title="Test", user=admin_user, avatar=wagtail_image)
        page.show_in_menus = True
        page.menu_icon = ""
        with pytest.raises(Exception, match="Menu Icon must be set"):
            page.clean()

    def test_clean_passes_when_in_menu_with_icon(self, db, admin_user, wagtail_image):
        page = BasePage(title="Test", user=admin_user, avatar=wagtail_image)
        page.show_in_menus = True
        page.menu_icon = "some-icon"
        page.clean()


class TestBasePageGetContext:
    def test_context_has_skip_intro_default(self, rf, db, admin_user, root_page, wagtail_image):
        page = BasePage(title="Test", user=admin_user, avatar=wagtail_image)
        root_page.add_child(instance=page)
        request = HttpRequest()
        request.GET = {}
        context = page.get_context(request)
        assert context["skip_intro"] is False

    def test_context_has_skip_intro_when_set(self, rf, db, admin_user, root_page, wagtail_image):
        page = BasePage(title="Test", user=admin_user, avatar=wagtail_image)
        root_page.add_child(instance=page)
        request = HttpRequest()
        request.GET = {"skip-intro": ""}
        context = page.get_context(request)
        assert context["skip_intro"] is True

    def test_context_has_menu_items(self, rf, db, admin_user, root_page, wagtail_image):
        page = BasePage(title="Test", user=admin_user, show_in_menus=True, menu_icon="icon", avatar=wagtail_image)
        root_page.add_child(instance=page)
        request = HttpRequest()
        request.GET = {}
        context = page.get_context(request)
        assert "menu_items" in context
