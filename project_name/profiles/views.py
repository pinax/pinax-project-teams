from django.core.urlresolvers import reverse
from django.views.generic import UpdateView

from django.contrib import messages

from account.mixins import LoginRequiredMixin

from .forms import ProfileForm
from .models import Profile


class ProfileEditView(LoginRequiredMixin, UpdateView):

    form_class = ProfileForm
    model = Profile

    def get_object(self):
        return self.request.user.get_profile()

    def get_success_url(self):
        return reverse("profiles_edit")

    def form_valid(self, form):
        response = super(ProfileEditView, self).form_valid(form)
        messages.success(self.request, "You successfully updated your profile.")
        return response
