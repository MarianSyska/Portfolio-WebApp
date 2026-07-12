from datetime import date, timedelta

import pytest
from django.http import HttpResponse
from django.test.client import RequestFactory
from home.middleware import TokenReferralMiddleware
from home.models.referral import ReferralToken, RequestLog


def get_response(request):
    return HttpResponse("ok")


@pytest.fixture
def rf():
    return RequestFactory()


class TestTokenReferralMiddleware:
    def test_sets_referral_token_from_query_param(self, db, referral_token):
        request = RequestFactory().get("/?ref=test_token_123")
        from django.contrib.sessions.backends.db import SessionStore
        request.session = SessionStore()
        request.session.create()
        middleware = TokenReferralMiddleware(get_response)
        middleware(request)
        assert request.session["referral-token"] == "test_token_123"

    def test_ignores_invalid_referral_token(self, db, referral_token):
        request = RequestFactory().get("/?ref=nonexistent")
        from django.contrib.sessions.backends.db import SessionStore
        request.session = SessionStore()
        request.session.create()
        middleware = TokenReferralMiddleware(get_response)
        middleware(request)
        assert request.session.get("referral-token") is None

    def test_ignores_expired_referral_token(self, db, expired_referral_token):
        request = RequestFactory().get("/?ref=expired_token")
        from django.contrib.sessions.backends.db import SessionStore
        request.session = SessionStore()
        request.session.create()
        middleware = TokenReferralMiddleware(get_response)
        middleware(request)
        assert request.session.get("referral-token") is None

    def test_clears_expired_session_token(self, db, expired_referral_token):
        request = RequestFactory().get("/")
        from django.contrib.sessions.backends.db import SessionStore
        request.session = SessionStore()
        request.session.create()
        request.session["referral-token"] = "expired_token"
        middleware = TokenReferralMiddleware(get_response)
        middleware(request)
        assert request.session["referral-token"] is None

    def test_creates_request_log(self, db, referral_token):
        request = RequestFactory().get("/?ref=test_token_123")
        from django.contrib.sessions.backends.db import SessionStore
        request.session = SessionStore()
        request.session.create()
        middleware = TokenReferralMiddleware(get_response)
        middleware(request)
        assert RequestLog.objects.count() >= 1

    def test_keeps_valid_session_token(self, db, referral_token):
        request = RequestFactory().get("/")
        from django.contrib.sessions.backends.db import SessionStore
        request.session = SessionStore()
        request.session.create()
        request.session["referral-token"] = "test_token_123"
        middleware = TokenReferralMiddleware(get_response)
        middleware(request)
        assert request.session["referral-token"] == "test_token_123"

    def test_does_not_overwrite_same_token(self, db, referral_token):
        request = RequestFactory().get("/?ref=test_token_123")
        from django.contrib.sessions.backends.db import SessionStore
        request.session = SessionStore()
        request.session.create()
        request.session["referral-token"] = "test_token_123"
        middleware = TokenReferralMiddleware(get_response)
        middleware(request)
        assert request.session["referral-token"] == "test_token_123"

    def test_returns_response(self, db):
        request = RequestFactory().get("/")
        from django.contrib.sessions.backends.db import SessionStore
        request.session = SessionStore()
        request.session.create()
        middleware = TokenReferralMiddleware(get_response)
        response = middleware(request)
        assert response.status_code == 200
        assert response.content == b"ok"
