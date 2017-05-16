from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class TorrentBoxCreateForm(UserCreationForm):
    error_messages = {}
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username',
            }
        )
    )

    password1 = forms.CharField(
        required=True,
        min_length=6,
        widget=forms.widgets.PasswordInput(
            attrs={
                'placeholder': 'Password (At least 6 characters)',
            }
        )
    )

    password2 = forms.CharField(
        required=True,
        min_length=6,
        widget=forms.widgets.PasswordInput(
            attrs={
                'placeholder': 'Confirm password',
            }
        )
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def clean_username(self):
            return self.cleaned_data.get('username')


class TorrentBoxAuthForm(AuthenticationForm):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username',
            }
        )
    )

    password = forms.CharField(
        required=True,
        min_length=6,
        widget=forms.widgets.PasswordInput(
            attrs={
                'placeholder': 'Password',
            }
        )
    )
