from wagtail import hooks
from wagtail.snippets.models import register_snippet

from .views import CVViewSetGroup, PortfolioItemViewSet, ReferralTokenViewSet

register_snippet(ReferralTokenViewSet)


register_snippet(PortfolioItemViewSet)


register_snippet(CVViewSetGroup)


@hooks.register("register_icons")
def register_icons(icons: list[str]) -> list[str]:
    icons.append("home/icons/lightbulb-fill.svg")
    icons.append("home/icons/mortarboard.svg")
    icons.append("home/icons/person-in-suit.svg")
    icons.append("home/icons/tag.svg")
    return icons
