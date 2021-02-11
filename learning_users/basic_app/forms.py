from django import forms 
from django.contrib.auth.models import User
from basic_app.models import UserProfileInfo

class UserForm(forms.ModelForm):
	# we want to edit the builtin password field
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta():
		model = User
		# fields to include in the form
		fields = ('username', 'email','password')


class UserProfileForm(forms.ModelForm):
	class Meta():
		model = UserProfileInfo
		fields = ('portfolio_site', 'profile_pic')