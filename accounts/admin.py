from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from accounts.models import User


# Admin Forms

class UserCreationAdminForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username',)


class UserChangeAdminForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('username',)


# Admin Registeration

admin.site.unregister(Group)


@admin.register(User)
class AdvanceUserAdmin(UserAdmin):
    form = UserChangeAdminForm
    add_form = UserCreationAdminForm
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'email', 'bio', 'birthday', 'picture')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'email_verified')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'), }),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'email', 'bio', 'birthday', 'picture')}),
    )
