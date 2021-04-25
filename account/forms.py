from django.db.models import fields
from .models import FaultEntry, FaultLocation, MyUser, Runway
from django.contrib.auth import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UsernameField, PasswordResetForm, SetPasswordForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms
from django.db import models
from django.forms import widgets
from django.forms.widgets import PasswordInput
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget


class CreateUserForm(UserCreationForm):
    password1 = forms.CharField(widget=PasswordInput(
        attrs={'class': 'form-control'}), label='Password')
    password2 = forms.CharField(widget=PasswordInput(
        attrs={'class': 'form-control'}), label='Confirm Password')

    class Meta:
        model = MyUser
        fields = ['user_name', 'first_name', 'last_name', 'email', 'airport']
        labels = {'email': 'Email', 'first_name': 'First Name',
                  'last_name': 'Last Name'}

        widgets = {'user_name': forms.TextInput(attrs={'class': 'form-control'}),
                   'first_name': forms.TextInput(attrs={'class': 'form-control'}),
                   'last_name': forms.TextInput(attrs={'class': 'form-control'}),
                   'email': forms.EmailInput(attrs={'class': 'form-control'}),
                   'airport': forms.Select(attrs={'class': 'form-control'}),
                   }


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(
        attrs={'autofocus': True, 'class': 'form-control'}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'current-password', 'class': 'form-control'}),
    )

    error_messages = {
        'invalid_login': _(
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': _("This account is not verified."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)


class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email',
        'type': 'email',
        'name': 'email'
    }))


class UserSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        strip=False,

    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
    )


class UserChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'current-password', 'autofocus': True, 'class': 'form-control'}),
    )
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        strip=False,

    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
    )

    field_order = ['old_password', 'new_password1', 'new_password2']


class EditUserForm(UserChangeForm):
    password = None

    class Meta:
        model = MyUser
        fields = ['user_name', 'first_name', 'last_name',
                  'email', 'phone', 'address', 'image']
        labels = {'email': 'Email', 'first_name': 'First Name',
                  'last_name': 'Last Name'}

        widgets = {'user_name': forms.TextInput(attrs={'class': 'form-control'}),
                   'first_name': forms.TextInput(attrs={'class': 'form-control'}),
                   'last_name': forms.TextInput(attrs={'class': 'form-control'}),
                   'email': forms.EmailInput(attrs={'class': 'form-control'}),
                   'phone': forms.TextInput(attrs={'class': 'form-control'}),
                   'address': forms.TextInput(attrs={'class': 'form-control'}),
                   }


class FaultEntryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(FaultEntryForm, self).__init__(*args, **kwargs)
        if user is not None and not user.is_superuser:
            self.fields['location'].queryset = FaultLocation.objects.filter(
                airport=user.airport)
            self.fields['runway'].queryset = Runway.objects.filter(
                airport=user.airport)

    class Meta:
        model = FaultEntry

        fields = ['equipment', 'runway', 'start_date', 'end_date', 'start_time',
                  'end_time', 'location', 'fault_discription', 'action_taken']
        labels = {'location': 'Fault Location', }
        widgets = {
            'start_date': forms.DateInput(attrs={'class': 'dateinput form-control'}),
            'end_date': forms.DateInput(attrs={'class': 'dateinput form-control'}),
            'start_time': forms.TimeInput(attrs={'class': 'timeinput form-control'}),
            'end_time': forms.TimeInput(attrs={'class': 'timeinput form-control'}),
            'fault_discription': forms.Textarea(attrs={'class': 'form-control', 'rows': '6'}),
            'action_taken': forms.Textarea(attrs={'class': 'form-control', 'rows': '6'}),
        }

class RunwayForm(forms.ModelForm):
    class Meta:
        model = Runway
        fields = ['runway']
        widgets = {
            'runway': forms.DateInput(attrs={'class': 'form-control'}),
            
        }