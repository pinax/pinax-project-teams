from django.test import TestCase

from django.contrib.auth.models import User

from .models import Team, Membership


class BaseTeamTests(TestCase):

    MANAGER_ACCESS = Team.MANAGER_ACCESS_ADD
    MEMBER_ACCESS = Team.MEMBER_ACCESS_OPEN

    def _create_team(self):
        return Team.objects.create(
            name="Eldarion",
            creator=self.user,
            manager_access=self.MANAGER_ACCESS,
            member_access=self.MEMBER_ACCESS
        )

    def setUp(self):
        self.user = User.objects.create_user(username="jtauber")


class TeamTests(BaseTeamTests):

    def test_team_creation(self):
        team = self._create_team()
        self.assertEquals(team.name, "Eldarion")
        self.assertEquals(team.slug, "eldarion")
        self.assertEquals(team.creator, self.user)

    def test_team_unicode(self):
        team = self._create_team()
        self.assertEquals(str(team), "Eldarion")

    def test_team_creation_owner_is_member(self):
        team = self._create_team()
        team_user = team.memberships.all()[0]
        self.assertEquals(str(team_user), "jtauber in Eldarion")

    def test_team_role_for(self):
        team = self._create_team()
        self.assertEquals(team.role_for(self.user), Membership.ROLE_OWNER)

    def test_unknown_user(self):
        team = self._create_team()
        other_user = User.objects.create_user(username="paltman")
        self.assertIsNone(team.for_user(other_user))
        self.assertIsNone(team.role_for(other_user))

    def test_user_is_member(self):
        team = self._create_team()
        other_user = User.objects.create_user(username="paltman")
        team.add_user(other_user, Membership.ROLE_MEMBER)
        self.assertTrue(team.is_on_team(other_user))

    def test_owner_is_member(self):
        team = self._create_team()
        self.assertTrue(team.is_on_team(self.user))


class ManagerAddMemberOpenTests(BaseTeamTests):

    MANAGER_ACCESS = Team.MANAGER_ACCESS_ADD
    MEMBER_ACCESS = Team.MEMBER_ACCESS_OPEN

    def test_non_manager_adds_on_site_user(self):
        pass

    def test_manager_adds_on_site_user(self):
        pass

    def test_non_manager_adds_off_site_user(self):
        pass

    def test_manager_adds_off_site_user(self):
        pass

    def test_non_member_attempts_to_join(self):
        pass

    def test_non_member_applies_to_join(self):
        pass


class ManagerAddMemberApplicationTests(BaseTeamTests):

    MANAGER_ACCESS = Team.MANAGER_ACCESS_ADD
    MEMBER_ACCESS = Team.MEMBER_ACCESS_APPLICATION

    def test_non_manager_adds_on_site_user(self):
        pass

    def test_manager_adds_on_site_user(self):
        pass

    def test_non_manager_adds_off_site_user(self):
        pass

    def test_manager_adds_off_site_user(self):
        pass

    def test_non_member_attempts_to_join(self):
        pass

    def test_non_member_applies_to_join(self):
        pass


class ManagerAddMemberInvitationTests(BaseTeamTests):

    MANAGER_ACCESS = Team.MANAGER_ACCESS_ADD
    MEMBER_ACCESS = Team.MEMBER_ACCESS_INVITATION

    def test_non_manager_adds_on_site_user(self):
        pass

    def test_manager_adds_on_site_user(self):
        pass

    def test_non_manager_adds_off_site_user(self):
        pass

    def test_manager_adds_off_site_user(self):
        pass

    def test_non_member_attempts_to_join(self):
        pass

    def test_non_member_applies_to_join(self):
        pass


class ManagerInviteMemberOpenTests(BaseTeamTests):

    MANAGER_ACCESS = Team.MANAGER_ACCESS_INVITE
    MEMBER_ACCESS = Team.MEMBER_ACCESS_OPEN

    def test_non_manager_adds_on_site_user(self):
        pass

    def test_manager_adds_on_site_user(self):
        pass

    def test_non_manager_adds_off_site_user(self):
        pass

    def test_manager_adds_off_site_user(self):
        pass

    def test_non_member_attempts_to_join(self):
        pass

    def test_non_member_applies_to_join(self):
        pass


class ManagerInviteMemberApplicationTests(BaseTeamTests):

    MANAGER_ACCESS = Team.MANAGER_ACCESS_INVITE
    MEMBER_ACCESS = Team.MEMBER_ACCESS_APPLICATION

    def test_non_manager_adds_on_site_user(self):
        pass

    def test_manager_adds_on_site_user(self):
        pass

    def test_non_manager_adds_off_site_user(self):
        pass

    def test_manager_adds_off_site_user(self):
        pass

    def test_non_member_attempts_to_join(self):
        pass

    def test_non_member_applies_to_join(self):
        pass


class ManagerInviteMemberInvitationTests(BaseTeamTests):

    MANAGER_ACCESS = Team.MANAGER_ACCESS_INVITE
    MEMBER_ACCESS = Team.MEMBER_ACCESS_INVITATION

    def test_non_manager_adds_on_site_user(self):
        pass

    def test_manager_adds_on_site_user(self):
        pass

    def test_non_manager_adds_off_site_user(self):
        pass

    def test_manager_adds_off_site_user(self):
        pass

    def test_non_member_attempts_to_join(self):
        pass

    def test_non_member_applies_to_join(self):
        pass
