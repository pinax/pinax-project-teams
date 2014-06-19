from django.conf.urls import patterns, url

from .views import TeamCreateView, TeamUpdateView


urlpatterns = patterns(
    "project_name.teams.views",

    # overall
    url(r"^:create/$", TeamCreateView.as_view(), name="team_create"),

    # team specific
    url(r"^(?P<slug>[\w\-]+)/$", "team_detail", name="team_detail"),
    url(r"^(?P<slug>[\w\-]+)/join/$", "team_join", name="team_join"),
    url(r"^(?P<slug>[\w\-]+)/leave/$", "team_leave", name="team_leave"),
    url(r"^(?P<slug>[\w\-]+)/apply/$", "team_apply", name="team_apply"),
    url(r"^(?P<slug>[\w\-]+)/edit/$", TeamUpdateView.as_view(), name="team_edit"),

    # membership specific
    url(r"^promote/(?P<pk>\d+)/$", "team_promote", name="team_promote"),
    url(r"^demote/(?P<pk>\d+)/$", "team_demote", name="team_demote"),
    url(r"^accept/(?P<pk>\d+)/$", "team_accept", name="team_accept"),
    url(r"^reject/(?P<pk>\d+)/$", "team_reject", name="team_reject"),
)
