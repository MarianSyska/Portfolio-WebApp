import pytest
from home.views import (
    CVViewSetGroup,
    EducationViewSet,
    ExperienceViewSet,
    PortfolioItemViewSet,
    ReferralTokenViewSet,
    SkillItemViewSet,
)


class TestReferralTokenViewSet:
    def test_model(self):
        from home.models import ReferralToken
        assert ReferralTokenViewSet.model == ReferralToken

    def test_add_to_settings_menu(self):
        assert ReferralTokenViewSet.add_to_settings_menu is True

    def test_copy_view_disabled(self):
        assert ReferralTokenViewSet.copy_view_enabled is False

    def test_list_display(self):
        assert ReferralTokenViewSet.list_display == ["id", "title", "description", "expire_date", "level"]


class TestPortfolioItemViewSet:
    def test_model(self):
        from home.models import PortfolioItem
        assert PortfolioItemViewSet.model == PortfolioItem

    def test_menu_label(self):
        assert PortfolioItemViewSet.menu_label == "Portfolio"

    def test_add_to_admin_menu(self):
        assert PortfolioItemViewSet.add_to_admin_menu is True

    def test_copy_view_disabled(self):
        assert PortfolioItemViewSet.copy_view_enabled is False


class TestExperienceViewSet:
    def test_model(self):
        from home.models import JobItem
        assert ExperienceViewSet.model == JobItem

    def test_menu_label(self):
        assert ExperienceViewSet.menu_label == "Experience"

    def test_add_to_admin_menu(self):
        assert ExperienceViewSet.add_to_admin_menu is False

    def test_list_display(self):
        assert ExperienceViewSet.list_display == ["role", "company", "employment_date", "termination_date"]


class TestEducationViewSet:
    def test_model(self):
        from home.models import EducationItem
        assert EducationViewSet.model == EducationItem


class TestSkillItemViewSet:
    def test_model(self):
        from home.models import SkillDescriptionItem
        assert SkillItemViewSet.model == SkillDescriptionItem


class TestCVViewSetGroup:
    def test_items(self):
        assert CVViewSetGroup.items == [ExperienceViewSet, EducationViewSet, SkillItemViewSet]

    def test_add_to_admin_menu(self):
        assert CVViewSetGroup.add_to_admin_menu is True

    def test_menu_label(self):
        assert CVViewSetGroup.menu_label == "CV"
