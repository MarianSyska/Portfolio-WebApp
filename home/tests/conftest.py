from datetime import date, timedelta
from io import BytesIO

import pytest
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.test import Client
from PIL import Image as PILImage
from wagtail.images import get_image_model
from wagtail.models import Collection, Page, Site

from home.models.cv.education_item import EducationItem
from home.models.cv.job_item import JobItem
from home.models.referral import ReferralToken

User = get_user_model()
ImageModel = get_image_model()


@pytest.fixture(autouse=True)
def root_collection(db):
    root = Collection.add_root(name="Root")
    return root


@pytest.fixture
def wagtail_image(db, root_collection):
    pil_img = PILImage.new("RGB", (1, 1), color=(255, 0, 0))
    buffer = BytesIO()
    pil_img.save(buffer, format="jpeg")
    return ImageModel.objects.create(
        title="Test Image",
        file=ContentFile(buffer.getvalue(), name="test.jpg"),
    )


@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password="password",
    )


@pytest.fixture
def default_site(db):
    return Site.objects.get(is_default_site=True)


@pytest.fixture
def admin_client(admin_user):
    client = Client()
    client.force_login(admin_user)
    return client


@pytest.fixture
def root_page(default_site):
    return default_site.root_page


@pytest.fixture
def referral_token(db):
    return ReferralToken.objects.create(
        id="test_token_123",
        title="Test Token",
        description="A test referral token",
        level="L1",
        expire_date=date.today() + timedelta(days=30),
    )


@pytest.fixture
def expired_referral_token(db):
    return ReferralToken.objects.create(
        id="expired_token",
        title="Expired Token",
        level="L0",
        expire_date=date.today() - timedelta(days=1),
    )


@pytest.fixture
def job_item(db):
    return JobItem.objects.create(
        company="Test Corp",
        employment_date=date(2020, 1, 15),
        termination_date=date(2023, 6, 30),
        current_job=False,
        show_dates=True,
        role="Software Engineer",
        role_description="Built things.",
    )


@pytest.fixture
def current_job_item(db):
    return JobItem.objects.create(
        company="Current Inc",
        employment_date=date(2023, 7, 1),
        termination_date=date(2023, 7, 1),
        current_job=True,
        show_dates=True,
        role="Senior Engineer",
        role_description="Leading projects.",
    )


@pytest.fixture
def education_item(db):
    return EducationItem.objects.create(
        institution="University of Test",
        title="BSc Computer Science",
        grade="1.5",
        conclusion_date=date(2020, 8, 15),
    )
