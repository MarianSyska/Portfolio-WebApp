from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from .models import (
    EducationItem,
    JobItem,
    PortfolioItem,
    ReferralToken,
    SkillDescriptionItem,
)


class ReferralTokenViewSet(SnippetViewSet):
    model = ReferralToken
    icon = "tag"
    add_to_settings_menu = True
    copy_view_enabled = False
    list_display = ["id", "title", "description", "expire_date", "level"]  # noqa: RUF012


class PortfolioItemViewSet(SnippetViewSet):
    model = PortfolioItem
    icon = "code"
    menu_label = "Portfolio"
    add_to_admin_menu = True
    copy_view_enabled = False
    list_display = ["project_title"]  # noqa: RUF012


class ExperienceViewSet(SnippetViewSet):
    model = JobItem
    icon = "person-in-suit"
    menu_label = "Experience"
    add_to_admin_menu = False
    copy_view_enabled = False
    list_display = ["role", "company", "employment_date", "termination_date"]  # noqa: RUF012


class EducationViewSet(SnippetViewSet):
    model = EducationItem
    icon = "mortarboard"
    menu_label = "Education"
    add_to_admin_menu = False
    copy_view_enabled = False
    list_display = ["title", "institution"]  # noqa: RUF012


class SkillItemViewSet(SnippetViewSet):
    model = SkillDescriptionItem
    icon = "lightbulb"
    menu_label = "Skillset"
    add_to_admin_menu = False
    copy_view_enabled = False
    list_display = ["title"]  # noqa: RUF012


class CVViewSetGroup(SnippetViewSetGroup):
    items = [ExperienceViewSet, EducationViewSet, SkillItemViewSet]  # noqa: RUF012
    add_to_admin_menu = True
    menu_label = "CV"
    menu_icon = "doc-full"
