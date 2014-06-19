from django import forms

from .models import Revision


class PageForm(forms.ModelForm):

    message = forms.CharField(required=False, help_text="Leave a helpful message about your change")

    class Meta:
        model = Revision
        fields = [
            "content",
            "message"
        ]
