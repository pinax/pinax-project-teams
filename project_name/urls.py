from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView

from django.contrib import admin

from project_name.profiles.views import ProfileDetailView, ProfileEditView, ProfileListView


from .lookups import user_wiki_lookup, team_wiki_lookup


WIKI_SLUG = r"((([A-Z]+[a-z]+){2,})(/([A-Z]+[a-z]+){2,})*)"


urlpatterns = patterns(
    "",
    url(r"^$", TemplateView.as_view(template_name="homepage.html"), name="home"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^account/", include("account.urls")),

    url(r"^profile/edit/", ProfileEditView.as_view(), name="profiles_edit"),
    url(r"^u/$", ProfileListView.as_view(), name="profiles_list"),

    url(r"^u/(?P<username>[\w\._-]+)/$", ProfileDetailView.as_view(), name="profiles_detail"),
    url(r"^u/(?P<username>[\w\._-]+)/w/$", "project_name.wiki.views.index", {"wiki_lookup": user_wiki_lookup}, name="user_wiki_index"),
    url(r"^u/(?P<username>[\w\._-]+)/w/(?P<slug>%s)/$" % WIKI_SLUG, "project_name.wiki.views.page", {"wiki_lookup": user_wiki_lookup}, name="user_wiki_page"),
    url(r"^u/(?P<username>[\w\._-]+)/w/(?P<slug>%s)/edit/$" % WIKI_SLUG, "project_name.wiki.views.edit", {"wiki_lookup": user_wiki_lookup}, name="user_wiki_page_edit"),

    url(r"^t/", include("project_name.teams.urls")),
    url(r"^t/(?P<team_slug>[\w\-]+)/w/$", "project_name.wiki.views.index", {"wiki_lookup": team_wiki_lookup}, name="team_wiki_index"),
    url(r"^t/(?P<team_slug>[\w\-]+)/w/(?P<slug>%s)/$" % WIKI_SLUG, "project_name.wiki.views.page", {"wiki_lookup": team_wiki_lookup}, name="team_wiki_page"),
    url(r"^t/(?P<team_slug>[\w\-]+)/w/(?P<slug>%s)/edit/$" % WIKI_SLUG, "project_name.wiki.views.edit", {"wiki_lookup": team_wiki_lookup}, name="team_wiki_page_edit"),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
