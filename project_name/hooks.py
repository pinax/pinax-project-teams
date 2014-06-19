from django.core.urlresolvers import reverse

from project_name.wiki.hooks import WikiDefaultHookset


class ProjectWikiHookset(WikiDefaultHookset):

    def page_url(self, wiki, slug):
        if wiki.content_type.model == "user":
            user = wiki.content_type.get_object_for_this_type(pk=wiki.object_id)
            return reverse("user_wiki_page", kwargs={"username": user.username, "slug": slug})
        elif wiki.content_type.model == "team":
            team = wiki.content_type.get_object_for_this_type(pk=wiki.object_id)
            return reverse("team_wiki_page", kwargs={"team_slug": team.slug, "slug": slug})
        return "/"

    def page_edit_url(self, wiki, slug):
        if wiki.content_type.model == "user":
            user = wiki.content_type.get_object_for_this_type(pk=wiki.object_id)
            return reverse("user_wiki_page_edit", kwargs={"username": user.username, "slug": slug})
        elif wiki.content_type.model == "team":
            team = wiki.content_type.get_object_for_this_type(pk=wiki.object_id)
            return reverse("team_wiki_page_edit", kwargs={"team_slug": team.slug, "slug": slug})
        return "/"
