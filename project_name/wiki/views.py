from django.shortcuts import get_object_or_404, redirect, render

from project_name.teams.models import Team

from .conf import settings
from .forms import PageForm
from .models import Page


def index(request, slug):
    return redirect("wiki_page", slug=slug, page_slug="WikiIndex")


def page(request, slug, page_slug):
    team = get_object_or_404(Team, slug=slug)
    try:
        page = team.pages.get(slug=page_slug)
    except Page.DoesNotExist:
        return redirect("wiki_page_edit", slug=slug, page_slug=page_slug)
    rev = page.revisions.latest()
    return render(request, "wiki/page.html", {"revision": rev})


def edit(request, slug, page_slug):
    team = get_object_or_404(Team, slug=slug)
    try:
        page = team.pages.get(slug=page_slug)
        rev = page.revisions.latest()
        initial = {
            "content": rev.content
        }
    except Page.DoesNotExist:
        page = Page(team=team, slug=slug)
        rev = None
        initial = {
            "content": "add content and create a new page",
            "message": "initial revision"
        }
    if request.method == "POST":
        form = PageForm(request.POST)
        if form.is_valid():
            if initial["content"] == form.cleaned_data["content"]:
                form.errors["content"] = "You haven't made any changes!"
            else:
                if page.pk is None:
                    page.save()
                revision = form.save(commit=False)
                revision.page = page
                revision.created_by = request.user
                revision.created_ip = request.META.get(settings.WIKI_IP_ADDRESS_META_FIELD)
                revision.parse()
                revision.save()
                return redirect("wiki_page", slug=slug, page_slug=page_slug)
    else:
        form = PageForm(initial=initial)

    return render(request, "wiki/edit.html", {
        "form": form,
        "page": page,
        "revision": rev,
    })
