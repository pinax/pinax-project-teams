from django.core.urlresolvers import reverse

from project_name.wiki.hooks import WikiDefaultHookset


class ProjectWikiHookset(WikiDefaultHookset):

    def page_url(self, wiki, slug):
        if wiki.content_type.model == "user":
            user = wiki.content_type.get_object_for_this_type(pk=wiki.object_id)
            return reverse("wiki_page", kwargs={"username": user.username, "slug": slug})
        return "/"

    def page_edit_url(self, wiki, slug):
        if wiki.content_type.model == "user":
            user = wiki.content_type.get_object_for_this_type(pk=wiki.object_id)
            return reverse("wiki_page_edit", kwargs={"username": user.username, "slug": slug})
        return "/"
