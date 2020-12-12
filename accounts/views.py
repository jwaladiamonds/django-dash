from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import login, views
from django.views.generic.edit import CreateView
from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import login_required, permission_required
# from gmailer.gmail import mailer

from accounts.tools import activater
from accounts.forms import SignUpForm, LoginForm
from accounts.models import User

#
# @login_required
# @permission_required("is_staff", login_url='/dashboard/')
# def gmail(request):
#     request.session['oauth_state'] = mailer.auth_state
#     return redirect(mailer.auth_uri)
#
#
# @login_required
# @permission_required("is_staff", login_url='/dashboard/')
# def gmail_verify(request):
#     code = request.GET.get('code', '')
#     state = request.GET.get('state', '')
#     if code and request.session.has_key('oauth_state') and state == request.session['oauth_state']:
#         mailer.verify(code)
#     else:
#         messages.error(request, "Invalid code/state found.")
#     return redirect('dash:gmail')
#
#
# @login_required
# @permission_required("is_staff", login_url='/dashboard/')
# def gmail_revoke(request):
#     mailer.revoke()
#     return redirect('dash:gmail')


class UserLogin(views.LoginView):
    template_name = 'auth/login.html'
    authentication_form = LoginForm

    def form_valid(self, form):
        user = form.get_user()
        if user.email_verified:
            login(self.request, user)
            if not self.request.POST.get('remember_me', None):
                self.request.session.set_expiry(0)
            messages.info(self.request, f"You are now logged in as {user}")
        else:
            messages.error(self.request,
                           "Your email is not verified. Please verify your email to login")
            return redirect('auth:login')
        return redirect(self.get_success_url())


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'auth/signup.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return super().get(request, *args, **kwargs)
        return redirect('core:home')

    def form_valid(self, form):
        if mailer.activated:
            user = form.save()
            mailer.send_mail(
                "Django Verification Code",
                "Hi " + str(user) + ",\n\nClick this link to activate: " +
                self.request.build_absolute_uri(reverse('auth:verify_email', args=(
                    user, activater.make_token(user)))),
                [user.email])
            messages.success(self.request,
                             "An email is sent to your email. Please verify your email to login")
            return redirect('core:home')
        else:
            messages.error(self.request,
                           "Gmail is not activate. Contact site administrator.")
            return redirect('auth:signup')
        return redirect('core:home')


def user_manage_permission(user, username):
    if not user.is_staff:
        if user.username == username:
            return True
    else:
        if user.username != username:
            return True
    return False


@login_required
@permission_required("is_staff", login_url='/dashboard/')
def user_force_logout(request, username):
    user = User.objects.get(username=username)
    sessions = [s.delete() for s in Session.objects.all()
                if s.get_decoded().get('_auth_user_id') == str(user.id)]
    print(sessions)
    return redirect('dash:users')


def user_verify_email(request, username, token):
    user = User.objects.get(username=username)
    if activater.check_token(user, token):
        print(user, "is verified")
        user.email_verified = True
        user.save()
        messages.success(request, "Your email is verified successfully")
    if request.user.is_staff and request.user.is_authenticated:
        return redirect('dash:users')
    return redirect('auth:login')


@login_required
def user_disable(request, username):
    if user_manage_permission(request.user, username):
        user = User.objects.get(username=username)
        user.is_active = False
        user.save()
        messages.error(request, 'Profile successfully disabled.')
    else:
        messages.error(
            request, 'You are not allowed to perform this operation.')
    if request.user.is_staff:
        return redirect('dash:users')
    else:
        return redirect('dash:profile')


@login_required
def user_enable(request, username):
    if user_manage_permission(request.user, username):
        user = User.objects.get(username=username)
        user.is_active = True
        user.save()
        messages.success(request, 'Profile successfully enabled.')
    else:
        messages.error(
            request, 'You are not allowed to perform this operation.')
    if request.user.is_staff:
        return redirect('dash:users')
    else:
        return redirect('dash:profile')


@login_required
def user_delete(request, username):
    if user_manage_permission(request.user, username):
        user = User.objects.get(username=username)
        user.delete()
        messages.error(request, 'Profile successfully deleted.')
    else:
        messages.error(
            request, 'You are not allowed to perform this operation.')
    if request.user.is_staff:
        return redirect('dash:users')
    else:
        return redirect('dash:profile')


user_login = UserLogin.as_view(redirect_authenticated_user=True)
user_signup = SignUpView.as_view()
user_logout = views.LogoutView.as_view()
