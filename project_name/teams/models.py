import datetime
import os
import uuid

from django.db import models

from django.contrib.auth.models import User

import reversion

from slugify import slugify


def avatar_upload(instance, filename):
    ext = filename.split(".")[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join("avatars", filename)


class Team(models.Model):

    ACCESS_OPEN = "open"
    ACCESS_APPLICATION = "application"
    ACCESS_INVITATION = "invitation"

    ACCESS_CHOICES = [
        (ACCESS_OPEN, "open"),
        (ACCESS_APPLICATION, "by application"),
        (ACCESS_INVITATION, "by invitation")
    ]

    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to=avatar_upload, blank=True)
    description = models.TextField(blank=True)
    access = models.CharField(max_length=20, choices=ACCESS_CHOICES)
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
        return self.memberships.filter(state=Membership.STATE_APPLIED)

    def invitees(self):
        return self.memberships.filter(state=Membership.STATE_INVITED)

    def members(self):
        return self.memberships.filter(state=Membership.STATE_MEMBER)

    def managers(self):
        return self.memberships.filter(state=Membership.STATE_MANAGER)

    def is_on_team(self, user):
        return self.memberships.exclude(state__in=[
            Membership.STATE_APPLIED,
            Membership.STATE_INVITED,
            Membership.STATE_DECLINED,
            Membership.STATE_REJECTED
        ]).filter(
            user=user
        ).exists()

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)[:50]
        self.full_clean()
        super(Team, self).save(*args, **kwargs)


class Membership(models.Model):

    STATE_APPLIED = "applied"
    STATE_INVITED = "invited"
    STATE_DECLINED = "declined"
    STATE_REJECTED = "rejected"
    STATE_MEMBER = "member"
    STATE_MANAGER = "manager"

    STATE_CHOICES = [
        (STATE_APPLIED, "applied"),
        (STATE_INVITED, "invited"),
        (STATE_DECLINED, "declined"),
        (STATE_REJECTED, "rejected"),
        (STATE_MEMBER, "member"),
        (STATE_MANAGER, "manager"),
    ]

    user = models.ForeignKey(User, related_name="memberships")
    team = models.ForeignKey(Team, related_name="memberships")
    state = models.CharField(max_length=20, choices=STATE_CHOICES)
    message = models.TextField(blank=True)


reversion.register(Membership)
