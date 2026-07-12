from datetime import date
from unittest.mock import MagicMock

import pytest
from django.http import HttpRequest
from home.models.cv.education_item import EducationItem
from home.models.cv.job_item import JobItem
from home.models.cv.skill_description import SkillDescriptionItem
from home.models.pages.cv_page import CVPage


class TestCVPageGetContext:
    def test_context_has_job_items(self, rf, db, admin_user, root_page, job_item, wagtail_image):
        page = CVPage(title="CV", user=admin_user, linkedin_link="https://linkedin.com/in/test", avatar=wagtail_image)
        root_page.add_child(instance=page)
        request = HttpRequest()
        request.session = {}
        context = page.get_context(request)
        assert "job_items" in context
        assert list(context["job_items"]) == [job_item]

    def test_context_has_education_items(self, rf, db, admin_user, root_page, education_item, wagtail_image):
        page = CVPage(title="CV", user=admin_user, linkedin_link="https://linkedin.com/in/test", avatar=wagtail_image)
        root_page.add_child(instance=page)
        request = HttpRequest()
        request.session = {}
        context = page.get_context(request)
        assert "education_items" in context
        assert list(context["education_items"]) == [education_item]

    def test_context_has_skill_items(self, rf, db, admin_user, root_page, wagtail_image):
        skill = SkillDescriptionItem.objects.create(title="Python", live=True)
        page = CVPage(title="CV", user=admin_user, linkedin_link="https://linkedin.com/in/test", avatar=wagtail_image)
        root_page.add_child(instance=page)
        request = HttpRequest()
        request.session = {}
        context = page.get_context(request)
        assert "skill_description_items" in context
        assert list(context["skill_description_items"]) == [skill]

    def test_context_has_links(self, rf, db, admin_user, root_page, wagtail_image):
        page = CVPage(
            title="CV",
            user=admin_user,
            linkedin_link="https://linkedin.com/in/test",
            github_link="https://github.com/test",
            avatar=wagtail_image,
        )
        root_page.add_child(instance=page)
        request = HttpRequest()
        request.session = {}
        context = page.get_context(request)
        assert context["linkedin_link"] == "https://linkedin.com/in/test"
        assert context["github_link"] == "https://github.com/test"

    def test_show_private_info_when_authenticated(self, rf, db, admin_user, root_page, wagtail_image):
        page = CVPage(title="CV", user=admin_user, avatar=wagtail_image)
        root_page.add_child(instance=page)
        request = HttpRequest()
        request.session = {}
        request.user = admin_user
        context = page.get_context(request)
        assert context.get("show_private_information") is True

    def test_show_private_info_with_referral_token_non_l0(self, rf, db, admin_user, root_page, referral_token, wagtail_image):
        page = CVPage(title="CV", user=admin_user, avatar=wagtail_image)
        root_page.add_child(instance=page)
        request = HttpRequest()
        request.session = {"referral-token": "test_token_123"}
        request.user = type("User", (), {"is_authenticated": False})()
        context = page.get_context(request)
        assert context.get("show_private_information") is True

    def test_show_private_info_false_with_l0_token(self, rf, db, admin_user, root_page, wagtail_image):
        from home.models.referral import ReferralToken
        token = ReferralToken.objects.create(id="l0_token", title="Public", level="L0")
        page = CVPage(title="CV", user=admin_user, avatar=wagtail_image)
        root_page.add_child(instance=page)
        request = HttpRequest()
        request.session = {"referral-token": "l0_token"}
        request.user = type("User", (), {"is_authenticated": False})()
        context = page.get_context(request)
        assert context.get("show_private_information") is False

    def test_job_items_ordered_by_employment_date_desc(self, rf, db, admin_user, root_page, wagtail_image):
        older = JobItem.objects.create(
            company="Old", employment_date=date(2020, 1, 1), termination_date=date(2021, 1, 1),
            current_job=False, role="Jr",
        )
        newer = JobItem.objects.create(
            company="New", employment_date=date(2022, 1, 1), termination_date=date(2023, 1, 1),
            current_job=False, role="Sr",
        )
        page = CVPage(title="CV", user=admin_user, avatar=wagtail_image)
        root_page.add_child(instance=page)
        request = HttpRequest()
        request.session = {}
        context = page.get_context(request)
        assert list(context["job_items"]) == [newer, older]

    def test_education_items_ordered_by_conclusion_date_desc(self, rf, db, admin_user, root_page, wagtail_image):
        older = EducationItem.objects.create(
            institution="U1", title="BSc", conclusion_date=date(2020, 6, 1)
        )
        newer = EducationItem.objects.create(
            institution="U2", title="MSc", conclusion_date=date(2022, 6, 1)
        )
        page = CVPage(title="CV", user=admin_user, avatar=wagtail_image)
        root_page.add_child(instance=page)
        request = HttpRequest()
        request.session = {}
        context = page.get_context(request)
        assert list(context["education_items"]) == [newer, older]
