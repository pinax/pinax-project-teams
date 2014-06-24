from django.test import TestCase

from django.contrib.auth.models import User

from .models import Team, Membership


class TeamTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="jtauber")

    def test_team_creation(self):
        team = Team.objects.create(name="Eldarion", creator=self.user, manager_access=Team.MANAGER_ACCESS_ADD, member_access=Team.MEMBER_ACCESS_OPEN)
        self.assertEquals(team.name, "Eldarion")
        self.assertEquals(team.slug, "eldarion")
        self.assertEquals(team.creator, self.user)

    def test_team_unicode(self):
        team = Team.objects.create(name="Eldarion", creator=self.user, manager_access=Team.MANAGER_ACCESS_ADD, member_access=Team.MEMBER_ACCESS_OPEN)
        self.assertEquals(str(team), "Eldarion")

    def test_team_creation_owner_is_member(self):
        team = Team.objects.create(name="Eldarion", creator=self.user, manager_access=Team.MANAGER_ACCESS_ADD, member_access=Team.MEMBER_ACCESS_OPEN)
        team_user = team.memberships.all()[0]
        self.assertEquals(str(team_user), "jtauber in Eldarion")

    def test_team_role_for(self):
        team = Team.objects.create(name="Eldarion", creator=self.user, manager_access=Team.MANAGER_ACCESS_ADD, member_access=Team.MEMBER_ACCESS_OPEN)
        self.assertEquals(team.role_for(self.user), Membership.ROLE_OWNER)

    def test_unknown_user(self):
        team = Team.objects.create(name="Eldarion", creator=self.user, manager_access=Team.MANAGER_ACCESS_ADD, member_access=Team.MEMBER_ACCESS_OPEN)
        other_user = User.objects.create_user(username="paltman")
        self.assertIsNone(team.for_user(other_user))
        self.assertIsNone(team.role_for(other_user))

    def test_user_is_member(self):
        team = Team.objects.create(name="Eldarion", creator=self.user, manager_access=Team.MANAGER_ACCESS_ADD, member_access=Team.MEMBER_ACCESS_OPEN)
        other_user = User.objects.create_user(username="paltman")
        team.add_user(other_user, Membership.ROLE_MEMBER)
        self.assertTrue(team.is_on_team(other_user))

    def test_owner_is_member(self):
        team = Team.objects.create(name="Eldarion", creator=self.user, manager_access=Team.MANAGER_ACCESS_ADD, member_access=Team.MEMBER_ACCESS_OPEN)
        self.assertTrue(team.is_on_team(self.user))
