from django.shortcuts import render, redirect,HttpResponseRedirect

from django.contrib import messages

from .models import User
from . import models
import bcrypt

# Display the main page for registration or login
def display_form(request):

	if request.method=="POST":
		del request.session["email"]
		del request.session["name"]
	return render(request, "index.html")

# handles the logout button
def go_backhome(request):

	if "user_name" in request.session:
		del request.session["user_name"]
	return redirect("/")

# Handles the request post after registration , creating a new user
def create_user(request):

	if request.method == "POST":
		errors = User.objects.basic_validator(request.POST)
		request.session["usertype"] = request.POST['which_from']
		if len(errors) > 0:
			for key, value in errors.items():
				messages.error(request, value, extra_tags=key)
			return redirect("/")
		else:
			user = models.create_user(request.POST)
			request.session["user_name"] = user.first_name
			request.session["usertype"] = request.POST['which_from']
			return redirect('/success')

# This method handles the login by user and redirect to the wall page
def login_user(request):

	if request.method == "POST":
		errors = User.objects.login_validator(request.POST)
		request.session["usertype"] = request.POST['which_from']
		if len(errors) > 0:
			for key, value in errors.items():
				messages.error(request, value)
			return render(request, "index.html")
		else:
			user = User.objects.get(email_address = request.POST['emailaddress'])
			request.session["email"] = user.email_address
			request.session["name"]=user.first_name

			return redirect('/wall')

# renders the success page after registration
def success(request):

	if "user_name" not in request.session:
		return  HttpResponseRedirect("you have to login")

	usertype=request.session["usertype"]
	name = request.session["user_name"]
	context = {
		"username": name,
		"usertype": usertype,
	}
	
	return render(request, "submit.html", context)
