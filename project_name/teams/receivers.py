from django.dispatch import receiver
from django.db.models.signals import post_save

from kaleo.signals import invite_accepted, joined_independently

from project_name.teams.models import Team, Membership


@receiver(post_save, sender=Team)
def handle_team_save(sender, **kwargs):
    created = kwargs.pop("created")
    team = kwargs.pop("instance")
    if created:
        team.add_user(team.creator, Membership.ROLE_OWNER)


@receiver([invite_accepted, joined_independently])
def handle_invite_used(sender, invitation, **kwargs):
    for membership in invitation.memberships.all():
        membership.joined()
