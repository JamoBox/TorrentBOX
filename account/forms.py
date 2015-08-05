from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Account 

class TorrentBoxCreateForm(UserCreationForm):
	username = forms.EmailField(widget=forms.widgets.EmailInput(attrs={'placeholder': 'Email address', 'required': 'true', 'autofocus': 'true'}))
	password1 = forms.CharField(min_length=3, widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password', 'required': 'true'}))
	password2 = forms.CharField(min_length=3, widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password confirm', 'required': 'true'}))

	class Meta:
		model = User
		fields = ('username', 'password1', 'password2')

	def save(self, commit=True):
		user = super(TorrentBoxCreateForm, self).save(commit=False)
		user.save()
		user_profile = Account(user=user)

		if commit:
			user_profile.save()

		return user_profile

	def is_valid(self):
		form = super(TorrentBoxCreateForm, self).is_valid()
		return form
		
	def clean_username(self):
		return self.cleaned_data.get('username')


class TorrentBoxAuthForm(AuthenticationForm):
	username = forms.EmailField(widget=forms.widgets.EmailInput(attrs={'placeholder': 'Email address', 'required': 'true', 'autofocus':'true'}))
	password = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password', 'required': 'true'}))

	def is_valid(self):
		form = super(TorrentBoxAuthForm, self).is_valid()
		return form
