from datetime import date, timedelta

import pytest
from django.contrib.sessions.models import Session
from django.db import IntegrityError
from django.utils import timezone
from home.models.referral import ReferralToken, RequestLog, default_expire_date, default_token


def create_session(session_key):
    return Session.objects.create(
        session_key=session_key,
        expire_date=timezone.now() + timedelta(days=1),
    )


class TestReferralToken:
    def test_str(self, referral_token):
        assert str(referral_token) == "Test Token"

    def test_default_token_length(self):
        token = default_token()
        assert len(token) <= 14

    def test_default_token_unique(self):
        tokens = {default_token() for _ in range(100)}
        assert len(tokens) == 100

    def test_default_expire_date(self):
        result = default_expire_date()
        expected = date.today() + timedelta(days=90)
        assert result == expected

    def test_created_date_auto_now_add(self, db):
        token = ReferralToken.objects.create(
            id="auto_date", title="Auto", level="L0",
            expire_date=date.today() + timedelta(days=10),
        )
        assert token.created_date == date.today()

    def test_expire_date_default(self, db):
        token = ReferralToken.objects.create(
            id="default_exp", title="Default Exp", level="L0"
        )
        expected = date.today() + timedelta(days=90)
        assert token.expire_date == expected

    def test_level_choices(self, db):
        token = ReferralToken.objects.create(
            id="l0", title="Public", level="L0",
            expire_date=date.today() + timedelta(days=10),
        )
        assert token.level == "L0"
        assert token.get_level_display() == "public"

    def test_description_blank_by_default(self, db):
        token = ReferralToken.objects.create(
            id="no_desc", title="No Description", level="L0",
            expire_date=date.today() + timedelta(days=10),
        )
        assert token.description == ""


class TestRequestLog:
    def test_default_view_count(self, referral_token, db):
        session = create_session("test_key")
        log = RequestLog.objects.create(
            referral_token=referral_token,
            session=session,
        )
        assert log.view_count == 0

    def test_last_viewed_null_by_default(self, referral_token, db):
        session = create_session("test_key2")
        log = RequestLog.objects.create(
            referral_token=referral_token,
            session=session,
        )
        assert log.last_viewed is None

    def test_unique_constraint(self, referral_token, db):
        session = create_session("unique_test")
        RequestLog.objects.create(
            referral_token=referral_token,
            session=session,
        )
        with pytest.raises(IntegrityError):
            RequestLog.objects.create(
                referral_token=referral_token,
                session=session,
            )

    def test_referral_token_nullable(self, db):
        session = create_session("null_token")
        log = RequestLog.objects.create(
            referral_token=None,
            session=session,
        )
        assert log.referral_token is None

    def test_session_nullable(self, referral_token, db):
        log = RequestLog.objects.create(
            referral_token=referral_token,
            session=None,
        )
        assert log.session is None
