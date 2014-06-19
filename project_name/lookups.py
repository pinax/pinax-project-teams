from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from project_name.wiki.models import Wiki


def user_wiki_lookup(*args, **kwargs):
    u = User.objects.get(username=kwargs.pop("username"))
    return Wiki.objects.get(
        content_type=ContentType.objects.get_for_model(u),
        object_id=u.pk
    )
