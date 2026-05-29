from django.http import Http404, HttpRequest, HttpResponse
from wagtail.models import Page


class SiteRootPage(Page):
        def route(self,
                  request: HttpRequest,
                  path_components: list[str]) -> HttpResponse:

            if not path_components:
                try:
                    target_page = self.get_children().get(slug="cv").specific
                except Page.DoesNotExist as e:
                    target_page = self.get_children().first()

                    if not target_page:
                        raise Http404 from e

                    target_page = target_page.specific

                return target_page.specific.route(request, path_components)

            return super().route(request, path_components)

        class Meta:
            verbose_name = "Site Root"
            proxy = True
