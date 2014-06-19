from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView

from django.contrib import admin

from project_name.profiles.views import ProfileDetailView, ProfileEditView


urlpatterns = patterns(
    "",
    url(r"^$", TemplateView.as_view(template_name="homepage.html"), name="home"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^account/", include("account.urls")),

    url(r"^profile/edit/", ProfileEditView.as_view(), name="profiles_edit"),
    url(r"^u/(?P<username>[\w\._-]+)/", ProfileDetailView.as_view(), name="profiles_detail")
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
