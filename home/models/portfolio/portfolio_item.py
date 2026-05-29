from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, PublishingPanel
from wagtail.models import DraftStateMixin, Orderable, RevisionMixin

from .technology_tag import TechnologyTag


class PortfolioItem(DraftStateMixin, RevisionMixin, Orderable, ClusterableModel):

    project_title = models.CharField(max_length=50)
    show_title = models.BooleanField("Show title on thumbnail", default=False)
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="Project Image",
    )
    description = models.TextField()
    tags = ClusterTaggableManager(through=TechnologyTag, blank=True)
    github_link = models.URLField(blank=True)
    revisions = GenericRelation("wagtailcore.Revision", related_query_name="+")


    panels = [  # noqa: RUF012
        FieldPanel("project_title"),
        FieldPanel("show_title"),
        FieldPanel("image"),
        FieldPanel("description"),
        FieldPanel("tags"),
        FieldPanel("github_link"),
        PublishingPanel(),
    ]


    def get_tags(self) -> ClusterTaggableManager[TechnologyTag]:
        return self.tags.get_queryset()


    def __str__(self) -> str:
        return self.project_title


    class Meta:
        ordering = ("sort_order",)
