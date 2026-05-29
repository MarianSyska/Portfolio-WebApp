from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import Manager
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, InlinePanel, PublishingPanel
from wagtail.models import DraftStateMixin, Orderable, RevisionMixin


class SkillSubSubDescriptionItem(Orderable):

    skill_item = ParentalKey("home.SkillSubDescriptionItem",
                             on_delete=models.CASCADE,
                             related_name="skill_subsubdescription_items")
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)


    panels = [  # noqa: RUF012
        FieldPanel("title"),
        FieldPanel("description"),
    ]


class SkillSubDescriptionItem(Orderable, ClusterableModel):

    skill_item = ParentalKey("home.SkillDescriptionItem",
                             on_delete=models.CASCADE,
                             related_name="skill_subdescription_items")
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)


    panels = [  # noqa: RUF012
        FieldPanel("title"),
        FieldPanel("description"),
        InlinePanel("skill_subsubdescription_items"),
    ]

    @property
    def subitems(self) -> Manager[SkillSubSubDescriptionItem]:
        return SkillSubSubDescriptionItem.objects.filter(skill_item=self)


class SkillDescriptionItem(DraftStateMixin, RevisionMixin, Orderable, ClusterableModel):

    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    revisions = GenericRelation("wagtailcore.Revision", related_query_name="+")


    panels = [  # noqa: RUF012
        FieldPanel("title"),
        FieldPanel("description"),
        InlinePanel("skill_subdescription_items"),
        PublishingPanel(),
    ]


    @property
    def subitems(self) -> Manager[SkillSubDescriptionItem]:
        return SkillSubDescriptionItem.objects.filter(skill_item=self)


    def __str__(self) -> str:
        return self.title


    class Meta:
        ordering = ("sort_order",)
