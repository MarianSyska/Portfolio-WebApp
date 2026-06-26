from io import StringIO

import pytest
from django.core.management import call_command

from home.models import EducationItem, JobItem, PortfolioItem, SkillDescriptionItem


class TestCreateMockDatabase:
    def test_creates_portfolio_items(self, db, default_site):
        out = StringIO()
        call_command("create_mock_database", stdout=out)
        assert PortfolioItem.objects.count() == 10

    def test_creates_skill_items(self, db, default_site):
        out = StringIO()
        call_command("create_mock_database", stdout=out)
        assert SkillDescriptionItem.objects.count() == 10

    def test_creates_education_items(self, db, default_site):
        out = StringIO()
        call_command("create_mock_database", stdout=out)
        assert 3 <= EducationItem.objects.count() <= 6

    def test_creates_job_items(self, db, default_site):
        out = StringIO()
        call_command("create_mock_database", stdout=out)
        assert 3 <= JobItem.objects.count() <= 6

    def test_creates_superuser(self, db, default_site):
        from django.contrib.auth import get_user_model

        User = get_user_model()
        out = StringIO()
        call_command("create_mock_database", stdout=out)
        assert User.objects.filter(is_superuser=True).exists()

    def test_creates_pages(self, db, default_site):
        from home.models.pages.cv_page import CVPage
        from home.models.pages.portfolio_page import PortfolioPage

        out = StringIO()
        call_command("create_mock_database", stdout=out)
        assert CVPage.objects.exists()
        assert PortfolioPage.objects.exists()
