import secrets
from datetime import datetime, timedelta

from django.contrib.sessions.models import Session
from django.db import models
from wagtail.admin.panels import FieldPanel


def default_expire_date() -> None:
        return datetime.now(tz=datetime.UTC).date() + timedelta(days=30*3)


def default_token() -> str:
    return secrets.token_urlsafe(14)


class ReferralToken(models.Model):

    id = models.CharField(max_length=14,
                          unique=True,
                          default=default_token,
                          primary_key=True)
    title = models.CharField(max_length=200)
    description =  models.TextField(blank=True)
    level = models.CharField(max_length=20, choices=[
        ("L0", "public"),
        ("L1", "restricted social media"),
        ("L2", "v-card"),
        ("L3", "private"),
    ])
    created_date = models.DateField(auto_now_add=True)
    expire_date = models.DateField(default=default_expire_date)

    panels = [  # noqa: RUF012
        FieldPanel("title"),
        FieldPanel("description"),
        FieldPanel("level"),
        FieldPanel("expire_date"),
    ]

    class Meta:
        verbose_name = "Referral Token"


    def __str__(self) -> str:
        return self.title


class RequestLog(models.Model):  # noqa: DJ008

    referral_token = models.ForeignKey(ReferralToken, on_delete=models.CASCADE, null=True)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True)
    last_viewed = models.DateField(null=True)
    view_count = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Request Log"
        constraints = [  # noqa: RUF012
            models.UniqueConstraint(fields=["referral_token", "session"],
                                    name="referral_token_session_uniqueness"),
        ]
