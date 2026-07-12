import pytest
from taggit.models import Tag

from home.models.portfolio.portfolio_item import PortfolioItem
from home.models.portfolio.technology_tag import TechnologyTag


class TestPortfolioItem:
    def test_str(self, db, wagtail_image):
        item = PortfolioItem.objects.create(
            project_title="My Project",
            image=wagtail_image,
            description="A great project.",
        )
        assert str(item) == "My Project"

    def test_get_tags_empty(self, db, wagtail_image):
        item = PortfolioItem.objects.create(
            project_title="No Tags",
            image=wagtail_image,
            description="No tags here.",
        )
        assert list(item.get_tags()) == []

    def test_get_tags_with_tags(self, db, wagtail_image):
        item = PortfolioItem.objects.create(
            project_title="Tagged",
            image=wagtail_image,
            description="Has tags.",
        )
        tag = Tag.objects.create(name="python")
        item.tags.add(tag)
        tags = item.get_tags()
        assert len(tags) == 1
        assert tags[0].name == "python"

    def test_show_title_default(self, db, wagtail_image):
        item = PortfolioItem.objects.create(
            project_title="Default",
            image=wagtail_image,
            description="Check defaults.",
        )
        assert item.show_title is False

    def test_github_link_blank_by_default(self, db, wagtail_image):
        item = PortfolioItem.objects.create(
            project_title="No Link",
            image=wagtail_image,
            description="No github.",
        )
        assert item.github_link == ""

    def test_sort_order_default(self, db, wagtail_image):
        item = PortfolioItem.objects.create(
            project_title="Ordered",
            image=wagtail_image,
            description="Default order.",
        )
        assert item.sort_order is None


class TestTechnologyTag:
    def test_tag_association(self, db, wagtail_image):
        item = PortfolioItem.objects.create(
            project_title="Tagged Item",
            image=wagtail_image,
            description="Desc",
        )
        tag = Tag.objects.create(name="django")
        item.tags.add(tag)
        item.save()
        assert list(item.tags.all()) == [tag]
        tt = TechnologyTag.objects.get()
        assert tt.content_object == item
        assert tt.tag == tag
