from django import forms

from .models import Revision


class RevisionForm(forms.ModelForm):

    revision_pk = forms.IntegerField(widget=forms.HiddenInput())
    message = forms.CharField(required=False, help_text="Leave a helpful message about your change")

    def __init__(self, *args, **kwargs):
        super(RevisionForm, self).__init__(*args, **kwargs)
        self.fields["revision_pk"].initial = self.instance.pk

    def clean_content(self):
        if self.cleaned_data["content"] == self.instance.content:
            raise forms.ValidationError("You made no stinking changes")
        return self.cleaned_data["content"]

    def clean(self):
        if self.cleaned_data["revision_pk"] != self.instance.pk:
            raise forms.ValidationError("Someone edited this before you")
        return self.cleaned_data

    class Meta:
        model = Revision
        fields = [
            "revision_pk",
            "content",
            "message"
        ]
