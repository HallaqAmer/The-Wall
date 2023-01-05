from django.shortcuts import render,redirect,HttpResponse


from datetime import datetime

from .models import Message,Comment
from . import models


# Display the wall page
def display_wall(request):

    if not "name" in request.session:
        return redirect("/")
    
    messages=models.get_all_messages()
    context = {
        "messages": messages,
        "name": request.session["name"],
    }

    return render(request,"wall.html",context)

# creates the message posted by some user
def post_message(request):
    if not "name" in request.session:
        return redirect("/")
    if request.method=="POST":
        email=request.session["email"]
        models.create_message(request.POST,email)
        return redirect("/wall")
    else:
        return redirect("/wall")

# creates the comment added by some user
def add_comment(request):
    if not "name" in request.session:
        return redirect("/")
    email=request.session["email"]
    models.create_comment(request.POST,email)
    return redirect("/wall")

# deletes a message by a user who owns that message
def delete_message(request):
    if not "name" in request.session:
        return redirect("/")
    if request.method=="POST":
        msgid=int(request.POST['msgid'])
        models.delete_message(msgid)
    return redirect("/wall")