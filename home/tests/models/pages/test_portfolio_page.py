import pytest
from django.http import HttpRequest
from home.models.pages.portfolio_page import PortfolioPage
from home.models.portfolio.portfolio_item import PortfolioItem


class TestPortfolioPageGetContext:
    def test_context_has_items(self, rf, db, admin_user, root_page, wagtail_image):
        item = PortfolioItem.objects.create(
            project_title="Project A",
            image=wagtail_image,
            description="Desc",
            live=True,
        )
        page = PortfolioPage(title="Portfolio", user=admin_user, avatar=wagtail_image)
        root_page.add_child(instance=page)
        request = HttpRequest()
        request.GET = {}
        context = page.get_context(request)
        assert "items" in context
        assert list(context["items"]) == [item]

    def test_context_filters_live_items(self, rf, db, admin_user, root_page, wagtail_image):
        live_item = PortfolioItem.objects.create(
            project_title="Live", image=wagtail_image, description="Desc", live=True
        )
        draft_item = PortfolioItem.objects.create(
            project_title="Draft", image=wagtail_image, description="Desc", live=False
        )
        page = PortfolioPage(title="Portfolio", user=admin_user, avatar=wagtail_image)
        root_page.add_child(instance=page)
        request = HttpRequest()
        request.GET = {}
        context = page.get_context(request)
        assert list(context["items"]) == [live_item]

    def test_context_items_ordered_by_sort_order(self, rf, db, admin_user, root_page, wagtail_image):
        second = PortfolioItem.objects.create(
            project_title="B", image=wagtail_image, description="Desc", live=True, sort_order=2
        )
        first = PortfolioItem.objects.create(
            project_title="A", image=wagtail_image, description="Desc", live=True, sort_order=1
        )
        page = PortfolioPage(title="Portfolio", user=admin_user, avatar=wagtail_image)
        root_page.add_child(instance=page)
        request = HttpRequest()
        request.GET = {}
        context = page.get_context(request)
        assert list(context["items"]) == [first, second]
