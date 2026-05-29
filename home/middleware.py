from django.contrib.sessions.models import Session
from django.db.models import F
from django.http.request import HttpRequest
from django.utils import timezone

from .models import ReferralToken, RequestLog


class TokenReferralMiddleware:
    def __init__(self, get_response: callable):
        self.get_response = get_response


    def __call__(self, request : HttpRequest):

        sent_referral_token_id = request.GET.get("ref")
        session_referral_token_id = request.session.get("referral-token")


        #Check and set referral token
        is_sent_referral_token_valid = ReferralToken.objects.filter(id=sent_referral_token_id,
                                                                    expire_date__gt=timezone.now().date()).exists()

        if is_sent_referral_token_valid and sent_referral_token_id != session_referral_token_id:
            request.session["referral-token"] = sent_referral_token_id
            request.session.modified = True
            session_referral_token_id = sent_referral_token_id


        #Delete token when expired
        is_session_referral_token_valid = ReferralToken.objects.filter(id=session_referral_token_id,
                                                                       expire_date__gt=timezone.now().date()).exists()

        if not is_session_referral_token_valid:
            request.session["referral-token"] = None
            request.session.modified = True
            session_referral_token_id = None


        #Log request statistics
        referral_token = ReferralToken.objects.filter(id=session_referral_token_id).first()
        session = Session.objects.filter(session_key=request.session.get("session_key")).first()
        request_log = RequestLog.objects.get_or_create(session=session,
                                                       referral_token=referral_token)[0]

        if session:
            if request.session.get("has_visited"):
                RequestLog.objects.filter(session=None,
                                          referral_token=
                                          (
                                            referral_token.update(view_count=F("view_count") - 1)
                                          ))
            if(request_log.last_viewed != timezone.now().date()):
                    request_log.view_count += 1
                    request_log.last_viewed = timezone.now().date()
        else:
            request.session["has_visited"] = True
            request_log.view_count += 1

        return self.get_response(request)

