from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from .conf import settings
from .hooks import hookset


class Wiki(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.IntegerField()


class Page(models.Model):
    wiki = models.ForeignKey(Wiki, related_name="pages")  # @@@ Could make
    slug = models.SlugField()

    def get_absolute_url(self):
        return hookset.page_url(self.wiki, self.slug)

    def get_edit_url(self):
        return hookset.page_edit_url(self.wiki, self.slug)

    class Meta:
        unique_together = [("wiki", "slug")]


# @@@ how should locking be enabled

class Revision(models.Model):
    page = models.ForeignKey(Page, related_name="revisions")
    content = models.TextField()
    content_html = models.TextField()
    message = models.TextField(blank=True)
    created_ip = models.IPAddressField()
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, related_name="revisions_created")

    def parse(self):
        self.content_html = settings.WIKI_PARSE(self.content)

    class Meta:
        get_latest_by = "created_at"
