from django.contrib.auth import get_user_model
from django.db import models
from django.forms import ValidationError
from django.http import HttpRequest
from wagtail.admin.panels import FieldPanel
from wagtail.models import Page
from django.contrib.auth.models import User

User = get_user_model()


def get_superuser():  # noqa: ANN201
    return User.objects.filter(is_superuser=True).order_by("date_joined").first()


class BasePage(Page):
        user = models.ForeignKey(
                User,
                null=False,
                blank=False,
                on_delete=models.CASCADE,
                related_name="+",
                default=get_superuser,
        )

        avatar = models.ForeignKey(
                "wagtailimages.Image",
                null=True,
                blank=False,
                on_delete=models.PROTECT,
                related_name="+",
        )

        subtext = models.CharField(
                max_length=200,
                null=False,
                blank=True,
                default="",
        )

        menu_icon = models.CharField(
                max_length=200,
                null=False,
                blank=True,
                default="",
        )

        promote_panels = Page.promote_panels + [
            FieldPanel("menu_icon"),
            FieldPanel("user", permission="superuser-only"),
            FieldPanel("avatar"),
            FieldPanel("subtext"),
        ]

        parent_page_types = []  # noqa: RUF012
        subpage_types = []  # noqa: RUF012


        def get_context(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> dict:
                context = super().get_context(request, *args, **kwargs)

                context["menu_items"] = (
                        BasePage.objects.live().in_menu()
                        | BasePage.objects.filter(id=self.id).in_menu()
                )

                context["skip_intro"] = "skip-intro" in request.GET

                return context


        def clean(self, *args: tuple, **kwargs: dict) -> None:
                super().clean(*args, **kwargs)

                if self.show_in_menus and self.menu_icon == "":
                        raise ValidationError({
                                        "menu_icon":
                                                ("Menu Icon must be set "
                                                 "when Show in Menus is enabled."),
                                })
