from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView, UpdateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required

from dashboard.forms import ProfileForm
from accounts.models import User
from accounts.tools import activater


@login_required
def home(request):
    return render(request, 'dashboard/pages/home.html')


@login_required
def profile(request):
    return render(request, 'dashboard/pages/profile.html')


@login_required
@permission_required("is_staff", login_url='/dashboard/')
def users(request):
    users = User.objects.filter(is_staff=False)
    for user in users:
        if not user.email_verified:
            user.hashed = activater.make_token(user)
        else:
            user.hashed = "Verified"
    return render(request, 'dashboard/pages/users.html', {'users': users})


@login_required
@permission_required("is_staff", login_url='/dashboard/')
def gmail(request):
    credentials = None
    # if mailer.activated:
    #     credentials = mailer.credentials
    #     credentials.email = mailer.email
    return render(request, 'dashboard/pages/gmail.html', {'credentials': credentials})


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'dashboard/pages/profile_edit.html'
    success_url = '/dashboard/profile'
    form_class = ProfileForm

    def get_object(self, *args, **kwargs):
        return get_object_or_404(User, pk=self.request.user.pk)


profile_edit = ProfileEditView.as_view()
