from django.db import models
from wagtail.admin.panels import FieldPanel


class EducationItem(models.Model):
    institution = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    grade = models.CharField(max_length=50, null=False, blank=True)
    conclusion_date = models.DateField(null=True, blank=True)

    panels = [  # noqa: RUF012
        FieldPanel("institution"),
        FieldPanel("title"),
        FieldPanel("grade"),
        FieldPanel("conclusion_date"),
    ]

    def __str__(self) -> str:
        return self.title + " at " + self.institution
