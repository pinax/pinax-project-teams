from django.core.urlresolvers import reverse

from project_name.wiki.hooks import WikiDefaultHookset


class ProjectWikiHookset(WikiDefaultHookset):

    def _perm_check(self, wiki, user):
        if wiki.content_type.model == "user":
            return wiki.content_object == user
        elif wiki.content_type.model == "team":
            return wiki.content_object.is_on_team(user)
        return False

    def can_create_page(self, wiki, user):
        return self._perm_check(wiki, user)

    def can_edit_page(self, page, user):
        return self._perm_check(page.wiki, user)

    def can_delete_page(self, page, user):
        return self._perm_check(page.wiki, user)

    def can_view_page(self, page, user):
        return True

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
