from django.dispatch import receiver
from django.db.models.signals import post_save

from project_name.teams.models import Team, Membership


@receiver(post_save, sender=Team)
def handle_team_save(sender, **kwargs):
    created = kwargs.pop("created")
    team = kwargs.pop("instance")
    if created:
        team.memberships.create(user=team.creator, state=Membership.STATE_MANAGER)
