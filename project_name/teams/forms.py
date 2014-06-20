from django import forms

from django.utils.html import escape
from django.utils.safestring import mark_safe

from django.contrib.auth.models import User

from .models import Membership, Team, create_slug


class TeamForm(forms.ModelForm):

    def clean_name(self):
        if Team.objects.filter(slug=create_slug(self.cleaned_data["name"])).exists():
            raise forms.ValidationError("Team with this name already exists")
        return self.cleaned_data["name"]

    class Meta:
        model = Team
        fields = [
            "name",
            "avatar",
            "description",
            "access",
        ]


class TeamInvitationForm(forms.Form):

    email = forms.EmailField(help_text="email address must be that of an account on this site")

    def __init__(self, *args, **kwargs):
        self.team = kwargs.pop("team")
        super(TeamInvitationForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(TeamInvitationForm, self).clean()
        email = cleaned_data.get("email")

        if email is None:
            raise forms.ValidationError("valid email address required")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # eventually we can invite them but for now assume they are
            # already on the site
            raise forms.ValidationError(mark_safe("no account with email address <b>%s</b> found on this site" % escape(email)))

        state = self.team.get_state_for_user(user)

        if state in [Membership.STATE_MEMBER, Membership.STATE_MANAGER]:
            raise forms.ValidationError("user already in team")

        if state in [Membership.STATE_INVITED]:
            raise forms.ValidationError("user already invited to team")

        self.user = user
        self.state = state

        return cleaned_data

    def invite(self):
        if self.state is None:
            Membership.objects.create(team=self.team, user=self.user, state=Membership.STATE_INVITED)
        elif self.state == Membership.STATE_APPLIED:
            # if they applied we shortcut invitation process
            membership = Membership.objects.filter(team=self.team, user=self.user)
            membership.update(state=Membership.STATE_MEMBER)
