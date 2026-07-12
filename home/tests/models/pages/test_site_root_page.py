import pytest
from django.http import Http404, HttpRequest
from home.models.pages.base_page import BasePage
from home.models.pages.cv_page import CVPage
from home.models.pages.site_root_page import SiteRootPage
from wagtail.models import Page


class TestSiteRootPageRoute:
    def test_redirects_to_cv_child_when_path_empty(self, admin_user, root_page, wagtail_image):
        site_root = root_page.add_child(instance=SiteRootPage(title="Root"))
        cv_page = site_root.add_child(instance=CVPage(title="CV", slug="cv", user=admin_user, avatar=wagtail_image))
        request = HttpRequest()
        result = site_root.route(request, [])
        assert result.page == cv_page

    def test_falls_back_to_first_child_when_no_cv(self, admin_user, root_page, wagtail_image):
        site_root = root_page.add_child(instance=SiteRootPage(title="Root"))
        other = site_root.add_child(instance=BasePage(title="Other", slug="other", user=admin_user, avatar=wagtail_image))
        request = HttpRequest()
        result = site_root.route(request, [])
        assert result.page == other

    def test_raises_404_when_no_children(self, admin_user, root_page):
        site_root = root_page.add_child(instance=SiteRootPage(title="Root"))
        request = HttpRequest()
        with pytest.raises(Http404):
            site_root.route(request, [])

    def test_delegates_to_super_when_path_not_empty(self, admin_user, root_page, wagtail_image):
        site_root = root_page.add_child(instance=SiteRootPage(title="Root"))
        child = site_root.add_child(instance=BasePage(title="About", slug="about", user=admin_user, avatar=wagtail_image))
        request = HttpRequest()
        result = site_root.route(request, ["about"])
        assert result.page == child
