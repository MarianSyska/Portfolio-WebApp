from django.db import models
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase


class TechnologyTag(TaggedItemBase):
    content_object = ParentalKey("home.PortfolioItem",
                                 on_delete=models.CASCADE,
                                 related_name="tagged_items")
