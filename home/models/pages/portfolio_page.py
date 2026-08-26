from django.http import HttpRequest

from home.models.pages.base_page import BasePage
from home.models.portfolio.portfolio_item import PortfolioItem


class PortfolioPage(BasePage):

    parent_page_types = ["home.SiteRootPage"]  # noqa: RUF012
    subpage_types = []  # noqa: RUF012


    def get_context(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> dict:

        context = super().get_context(request, *args, **kwargs)

        context["items"] = (PortfolioItem
                            .objects.
                            filter(live=True)
                            .order_by(
                                "-highlighted",
                                "sort_order")
                            .select_related("image")
                            .prefetch_related("tags"))


        return context


    class Meta:
        verbose_name = "Portfolio"
