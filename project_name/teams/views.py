from django.http import Http404, HttpResponseRedirect, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from account.mixins import LoginRequiredMixin

# from symposion.utils.mail import send_email

from .forms import TeamInvitationForm, TeamForm
from .models import Team, Membership


## perm checks
#
# @@@ these can be moved

def can_join(team, user):
    state = team.get_state_for_user(user)
    if team.access == Team.ACCESS_OPEN and state is None:
        return True
    elif state == Membership.STATE_INVITED:
        return True
    elif user.is_staff and state is None:
        return True
    else:
        return False


def can_leave(team, user):
    state = team.get_state_for_user(user)
    if state == Membership.STATE_MEMBER:  # managers can't leave at the moment
        return True
    else:
        return False


def can_apply(team, user):
    state = team.get_state_for_user(user)
    if team.access == Team.ACCESS_APPLICATION and state is None:
        return True
    else:
        return False


def can_invite(team, user):
    state = team.get_state_for_user(user)
    if team.access == Team.ACCESS_INVITATION:
        if state == Membership.STATE_MANAGER or user.is_staff:
            return True
    return False


## views


class TeamCreateView(LoginRequiredMixin, CreateView):

    form_class = TeamForm
    model = Team

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.creator = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class TeamUpdateView(LoginRequiredMixin, UpdateView):

    form_class = TeamForm
    model = Team


class TeamListView(ListView):

    model = Team
    context_object_name = "teams"


@login_required
def team_detail(request, slug):
    team = get_object_or_404(Team, slug=slug)
    state = team.get_state_for_user(request.user)
    if team.access == Team.ACCESS_INVITATION and state is None and not request.user.is_staff:
        raise Http404()

    if can_invite(team, request.user):
        if request.method == "POST":
            form = TeamInvitationForm(request.POST, team=team)
            if form.is_valid():
                form.invite()
                # send_email([form.user.email], "teams_user_invited", context={"team": team})
                messages.success(request, "Invitation created.")
                return redirect("team_detail", slug=slug)
        else:
            form = TeamInvitationForm(team=team)
    else:
        form = None

    return render(request, "teams/team_detail.html", {
        "team": team,
        "state": state,
        "invite_form": form,
        "can_join": can_join(team, request.user),
        "can_leave": can_leave(team, request.user),
        "can_apply": can_apply(team, request.user),
    })


@login_required
def team_join(request, slug):
    team = get_object_or_404(Team, slug=slug)
    state = team.get_state_for_user(request.user)
    if team.access == Team.ACCESS_INVITATION and state is None and not request.user.is_staff:
        raise Http404()

    if can_join(team, request.user) and request.method == "POST":
        membership, created = Membership.objects.get_or_create(team=team, user=request.user)
        membership.state = Membership.STATE_MEMBER
        membership.save()
        messages.success(request, "Joined team.")
        return redirect("team_detail", slug=slug)
    else:
        return redirect("team_detail", slug=slug)


@login_required
def team_leave(request, slug):
    team = get_object_or_404(Team, slug=slug)
    state = team.get_state_for_user(request.user)
    if team.access == Team.ACCESS_INVITATION and state is None and not request.user.is_staff:
        raise Http404()

    if can_leave(team, request.user) and request.method == "POST":
        membership = Membership.objects.get(team=team, user=request.user)
        membership.delete()
        messages.success(request, "Left team.")
        return redirect("dashboard")
    else:
        return redirect("team_detail", slug=slug)


@login_required
def team_apply(request, slug):
    team = get_object_or_404(Team, slug=slug)
    state = team.get_state_for_user(request.user)
    if team.access == Team.ACCESS_INVITATION and state is None and not request.user.is_staff:
        raise Http404()

    if can_apply(team, request.user) and request.method == "POST":
        membership, created = Membership.objects.get_or_create(team=team, user=request.user)
        membership.state = Membership.STATE_APPLIED
        membership.save()
        managers = [m.user.email for m in team.managers()]
        # send_email(managers, "teams_user_applied", context={
        #     "team": team,
        #     "user": request.user
        # })
        messages.success(request, "Applied to join team.")
        return redirect("team_detail", slug=slug)
    else:
        return redirect("team_detail", slug=slug)


@login_required
def team_promote(request, pk):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    membership = get_object_or_404(Membership, pk=pk)
    state = membership.team.get_state_for_user(request.user)
    if request.user.is_staff or state == Membership.STATE_MANAGER:
        if membership.state == Membership.STATE_MEMBER:
            membership.state = Membership.STATE_MANAGER
            membership.save()
            messages.success(request, "Promoted to manager.")
    return redirect("team_detail", slug=membership.team.slug)


@login_required
def team_demote(request, pk):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    membership = get_object_or_404(Membership, pk=pk)
    state = membership.team.get_state_for_user(request.user)
    if request.user.is_staff or state == Membership.STATE_MANAGER:
        if membership.state == Membership.STATE_MANAGER:
            membership.state = Membership.STATE_MEMBER
            membership.save()
            messages.success(request, "Demoted from manager.")
    return redirect("team_detail", slug=membership.team.slug)


@login_required
def team_accept(request, pk):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    membership = get_object_or_404(Membership, pk=pk)
    state = membership.team.get_state_for_user(request.user)
    if request.user.is_staff or state == Membership.STATE_MANAGER:
        if membership.state == Membership.STATE_APPLIED:
            membership.state = Membership.STATE_MEMBER
            membership.save()
            messages.success(request, "Accepted application.")
    return redirect("team_detail", slug=membership.team.slug)


@login_required
def team_reject(request, pk):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    membership = get_object_or_404(Membership, pk=pk)
    state = membership.team.get_state_for_user(request.user)
    if request.user.is_staff or state == Membership.STATE_MANAGER:
        if membership.state == Membership.STATE_APPLIED:
            membership.state = Membership.STATE_REJECTED
            membership.save()
            messages.success(request, "Rejected application.")
    return redirect("team_detail", slug=membership.team.slug)
