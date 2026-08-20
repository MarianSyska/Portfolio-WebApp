from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.models import Orderable, ParentalKey

from home.models.pages import CVPage


class CVLink(Orderable):
    cv_page = ParentalKey(CVPage, on_delete=models.CASCADE, related_name="links")
    title = models.CharField(max_length=255, primary_key=True)
    url = models.URLField()
    icon = models.CharField(max_length=255)

    panels = [
        FieldPanel("title"),
        FieldPanel("url"),
        FieldPanel("icon"),
    ]
