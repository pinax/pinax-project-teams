import datetime
import os
import uuid

from django.db import models

import reversion
from slugify import slugify

from django.contrib.auth.models import Permission, User


def avatar_upload(instance, filename):
    ext = filename.split(".")[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join("avatars", filename)


TEAM_ACCESS_CHOICES = [
    ("open", "open"),
    ("application", "by application"),
    ("invitation", "by invitation")
]


class Team(models.Model):

    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to=avatar_upload, blank=True)
    description = models.TextField(blank=True)
    access = models.CharField(max_length=20, choices=TEAM_ACCESS_CHOICES)

    # member permissions
    permissions = models.ManyToManyField(Permission, blank=True, related_name="member_teams")

    # manager permissions
    manager_permissions = models.ManyToManyField(Permission, blank=True, related_name="manager_teams")

    creator = models.ForeignKey(User, related_name="teams_created")
    created = models.DateTimeField(default=datetime.datetime.now, editable=False)

    @models.permalink
    def get_absolute_url(self):
        return ("team_detail", [self.slug])

    def __unicode__(self):
        return self.name

    def get_state_for_user(self, user):
        try:
            return self.memberships.get(user=user).state
        except Membership.DoesNotExist:
            return None

    def applicants(self):
        return self.memberships.filter(state="applied")

    def invitees(self):
        return self.memberships.filter(state="invited")

    def members(self):
        return self.memberships.filter(state="member")

    def managers(self):
        return self.memberships.filter(state="manager")

    def is_on_team(self, user):
        return self.memberships.exclude(state__in=["applied", "invited", "declined", "rejected"]).filter(user=user).exists()

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)[:50]
        self.full_clean()
        super(Team, self).save(*args, **kwargs)


MEMBERSHIP_STATE_CHOICES = [
    ("applied", "applied"),
    ("invited", "invited"),
    ("declined", "declined"),
    ("rejected", "rejected"),
    ("member", "member"),
    ("manager", "manager"),
]


class Membership(models.Model):

    STATE_MANAGER = "manager"
    user = models.ForeignKey(User, related_name="memberships")
    team = models.ForeignKey(Team, related_name="memberships")
    state = models.CharField(max_length=20, choices=MEMBERSHIP_STATE_CHOICES)
    message = models.TextField(blank=True)


reversion.register(Membership)
