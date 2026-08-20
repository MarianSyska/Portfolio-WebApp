from django.db import models
from django.http import HttpRequest
from wagtail.admin.panels import InlinePanel, MultiFieldPanel
from wagtail.models import Page

from home.models.cv.education_item import EducationItem
from home.models.cv.job_item import JobItem
from home.models.cv.skill_description import SkillDescriptionItem
from home.models.pages.base_page import BasePage
from home.models.referral import ReferralToken


class CVPage(BasePage):

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            InlinePanel('links'),
            ],
            heading="Personal Information",
        ),
    ]

    parent_page_types = ["home.SiteRootPage"]  # noqa: RUF012
    subpage_types = []  # noqa: RUF012


    def get_context(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> dict:

        context = super().get_context(request, *args, **kwargs)

        referral_token = request.session.get("referral-token")
        if referral_token:
            context["show_private_information"] = (
                ReferralToken.objects.get(id=referral_token).level != "L0"
            )
        elif self.user.is_authenticated:
            context["show_private_information"] = True

        context["job_items"] = (JobItem
                                .objects
                                .all()
                                .order_by("employment_date")
                                .reverse())
        context["education_items"] = (EducationItem
                                      .objects
                                      .all()
                                      .order_by("conclusion_date")
                                      .reverse())
        context["skill_description_items"] = (
            SkillDescriptionItem.objects.filter(live=True)
        )

        return context


    class Meta:
        verbose_name = "CV"
