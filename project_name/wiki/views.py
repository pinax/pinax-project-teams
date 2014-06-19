from django.http import Http404, HttpResponseForbidden
from django.shortcuts import redirect, render

from .conf import settings
from .forms import PageForm
from .hooks import hookset
from .models import Page


def index(request, wiki_lookup, *args, **kwargs):
    wiki = wiki_lookup(*args, **kwargs)
    return redirect(hookset.page_url(wiki, "WikiIndex"))


def page(request, slug, wiki_lookup, *args, **kwargs):
    wiki = wiki_lookup(*args, **kwargs)
    try:
        page = wiki.pages.get(slug=slug)
        if not hookset.can_view_page(page, request.user):
            raise Http404()
        rev = page.revisions.latest()
        return render(request, "wiki/page.html", {"revision": rev, "can_edit": hookset.can_edit_page(page, request.user)})
    except Page.DoesNotExist:
        return redirect(hookset.page_edit_url(wiki, slug))


def edit(request, slug, wiki_lookup, *args, **kwargs):
    wiki = wiki_lookup(*args, **kwargs)
    try:
        page = wiki.pages.get(slug=slug)
        rev = page.revisions.latest()
        initial = {
            "content": rev.content
        }
        if not hookset.can_edit_page(page, request.user):
            return HttpResponseForbidden()
    except Page.DoesNotExist:
        page = Page(wiki=wiki, slug=slug)
        rev = None
        initial = {
            "content": "add content and create a new page",
            "message": "initial revision"
        }
        if not hookset.can_edit_page(page, request.user):
            raise Http404()
    if request.method == "POST":
        form = PageForm(request.POST)
        if form.is_valid():
            if initial["content"] == form.cleaned_data["content"]:
                form.errors["content"] = ["You haven't made any changes!"]
            else:
                if page.pk is None:
                    page.save()
                revision = form.save(commit=False)
                revision.page = page
                revision.created_by = request.user
                revision.created_ip = request.META.get(settings.WIKI_IP_ADDRESS_META_FIELD, "REMOTE_ADDR")
                revision.parse()
                revision.save()
                return redirect(hookset.page_url(wiki, slug))
    else:
        form = PageForm(initial=initial)

    return render(request, "wiki/edit.html", {
        "form": form,
        "page": page,
        "revision": rev,
        "can_delete": hookset.can_delete_page(page, request.user)
    })
