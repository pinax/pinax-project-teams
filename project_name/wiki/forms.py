from django import forms

from .models import Revision


class PageForm(forms.ModelForm):

    class Meta:
        model = Revision
        fields = [
            "content",
            "message"
        ]
