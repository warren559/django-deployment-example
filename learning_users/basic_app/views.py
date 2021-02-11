from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileForm

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse

from django.urls import reverse
# if we want a view to require the user to be logged in 
from django.contrib.auth.decorators import login_required



# Create your views here.
def home(request):
	return render(request, 'basic_app/home.html')

@login_required
def special(request):
	return HttpResponse("You are logged in, Nice!!")

# we want to make sure that only a user who is logged in can log out
@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('basic_app:home'))


def register(request):

	# variable to indicate if someone is registered or not 
	registered = False

	if request.method == "POST":
		user_form = UserForm(data=request.POST) # contains the data from UserForm
		profile_form = UserProfileForm(data=request.POST) # contains the data from UserProfileForm

		# check if both the forms are valid
		if user_form.is_valid() and profile_form.is_valid():

			# save the user information to the database
			user = user_form.save()
			# hashing the password entered in by the user
			user.set_password(user.password)
			# save the hashed password to the database
			user.save()

			# save the extended user information to the database
			profile = profile_form.save(commit=False)

			# setup the one to one relationship with User
			profile.user = user

			# check if a profile picture was uploaded
			if 'profile_pic' in request.FILES:
				profile.profile_pic = request.FILES['profile_pic']

			profile.save()

			registered = True

		else: # both forms not valid
			print(user_form.errors, profile_form.errors)

	else:
		# not a post method - user did not fill in form yet, set everything up
		user_form = UserForm()
		profile_form = UserProfileForm()


	return render(request, "basic_app/registration.html",{
		"registered": registered,
		"user_form": user_form,
		"profile_form": profile_form
		})


def user_login(request):

	# if the form in login.html is submitted
	# get the username and password
	if request.method == "POST":
		username = request.POST.get("username")
		password = request.POST.get("password")

		# we going to use django's builtin authentication function to authenticate the user
		user = authenticate(username=username, password=password)

		if user: # if authentication is passed
			if user.is_active: # if the user is active (registered)
				login(request, user)# login user
				return HttpResponseRedirect(reverse('basic_app:home')) # return the user to a specific page 
			else:
				return HttpResponse("ACCOUNT NOT ACTIVE")
		else:
			print("Someone tried to login and failed")
			print("Username: {} and password {}".format(username, password))
			return HttpResponse("invalid login details supplied")

	else: # if the form is not submitted yet, just render the page 
		return render(request, 'basic_app/login.html')