from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User

from project_name.teams.models import Team

from .conf import settings


class Page(models.Model):
    team = models.ForeignKey(Team, related_name="pages")
    slug = models.SlugField()

    class Meta:
        unique_together = [("team", "slug")]


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
