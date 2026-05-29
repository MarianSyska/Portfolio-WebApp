import datetime

from dateutil.relativedelta import relativedelta
from django.db import models
from wagtail.admin.panels import FieldPanel


class JobItem(models.Model):
    company = models.CharField(max_length=50)
    employment_date = models.DateField()
    termination_date = models.DateField()
    current_job = models.BooleanField()
    show_dates = models.BooleanField(default=True)
    role = models.CharField(max_length=100)
    role_description = models.TextField(blank=True, default="")

    panels = [  # noqa: RUF012
        FieldPanel("company"),
        FieldPanel("employment_date"),
        FieldPanel("termination_date"),
        FieldPanel("current_job"),
        FieldPanel("show_dates"),
        FieldPanel("role"),
        FieldPanel("role_description"),
    ]

    def __str__(self) -> str:
        return (
            f"{self.role}"
            f"at {self.company}"
            f"from: {self.employment_date}"
            f"to: {self.termination_date}"
        )

    def employment_duration(self) -> str:
        duration = relativedelta(self.termination_date, self.employment_date)
        output_string = ""

        if self.show_dates:
            if self.current_job:
                output_string += f"{self.employment_date.strftime('%b %Y')} - Present"
            else:
                output_string += (f"{self.employment_date.strftime('%b %Y')}"
                                f" - {self.termination_date.strftime('%b %Y')}")

        if duration.years + duration.months > 0:
            if self.show_dates:
                output_string += " · "
            if duration.years == 1:
                output_string += f"{duration.years} Year"
            elif duration.years > 1:
                output_string += f"{duration.years} Years"
            if duration.months == 1:
                output_string += f" {duration.months} Month"
            elif duration.months > 1:
                output_string += f" {duration.months} Months"

        return output_string


