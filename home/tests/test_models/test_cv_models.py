from datetime import date

import pytest
from home.models.cv.education_item import EducationItem
from home.models.cv.job_item import JobItem
from home.models.cv.skill_description import (
    SkillDescriptionItem,
    SkillSubDescriptionItem,
    SkillSubSubDescriptionItem,
)


class TestJobItem:
    def test_str(self, job_item):
        expected = f"{job_item.role}at {job_item.company}from: {job_item.employment_date}to: {job_item.termination_date}"
        assert str(job_item) == expected

    def test_employment_duration_with_dates(self, job_item):
        result = job_item.employment_duration()
        assert "Jan 2020" in result
        assert "Jun 2023" in result
        assert "3 Years" in result
        assert "5 Months" in result

    def test_employment_duration_current_job(self, current_job_item):
        result = current_job_item.employment_duration()
        assert "Jul 2023" in result
        assert "Present" in result

    def test_employment_duration_dates_hidden(self, job_item):
        job_item.show_dates = False
        result = job_item.employment_duration()
        assert "Jan 2020" not in result
        assert "Jun 2023" not in result
        assert "3 Years" in result
        assert "5 Months" in result

    def test_employment_duration_single_year(self, db):
        item = JobItem.objects.create(
            company="Test",
            employment_date=date(2022, 1, 1),
            termination_date=date(2023, 1, 1),
            current_job=False,
            role="Dev",
        )
        result = item.employment_duration()
        assert "1 Year" in result
        assert "1 Year" not in result.replace("1 Year", "", 1)  # only one occurrence

    def test_employment_duration_single_month(self, db):
        item = JobItem.objects.create(
            company="Test",
            employment_date=date(2023, 1, 1),
            termination_date=date(2023, 2, 1),
            current_job=False,
            role="Dev",
        )
        result = item.employment_duration()
        assert "1 Month" in result


class TestEducationItem:
    def test_str(self, education_item):
        assert str(education_item) == "BSc Computer Science at University of Test"

    def test_str_blank_grade(self, db):
        item = EducationItem.objects.create(
            institution="MIT",
            title="PhD",
            grade="",
        )
        assert str(item) == "PhD at MIT"

    def test_null_conclusion_date(self, db):
        item = EducationItem.objects.create(
            institution="MIT",
            title="PhD",
            grade="",
            conclusion_date=None,
        )
        assert item.conclusion_date is None


class TestSkillDescriptionItem:
    def test_str(self, db):
        item = SkillDescriptionItem.objects.create(title="Python", description="Expert")
        assert str(item) == "Python"

    def test_subitems_property(self, db):
        parent = SkillDescriptionItem.objects.create(title="Parent")
        child = SkillSubDescriptionItem.objects.create(
            skill_item=parent,
            title="Child",
        )
        result = parent.subitems
        assert list(result) == [child]

    def test_subitems_empty(self, db):
        parent = SkillDescriptionItem.objects.create(title="Alone")
        assert list(parent.subitems) == []


class TestSkillSubDescriptionItem:
    def test_subitems_property(self, db):
        parent = SkillDescriptionItem.objects.create(title="Parent")
        sub = SkillSubDescriptionItem.objects.create(
            skill_item=parent,
            title="Sub",
        )
        sub_sub = SkillSubSubDescriptionItem.objects.create(
            skill_item=sub,
            title="SubSub",
        )
        result = sub.subitems
        assert list(result) == [sub_sub]

    def test_subitems_empty(self, db):
        parent = SkillDescriptionItem.objects.create(title="Parent")
        sub = SkillSubDescriptionItem.objects.create(
            skill_item=parent,
            title="Lonely",
        )
        assert list(sub.subitems) == []
