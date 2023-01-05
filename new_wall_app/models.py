from django.db import models
from login_app.models import User
from datetime import datetime





class Message(models.Model):
    message=models.TextField()
    user=models.ForeignKey(User,related_name="messages",on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class Comment(models.Model):
    comment=models.TextField()
    user=models.ForeignKey(User,related_name="comments",on_delete=models.CASCADE)
    message=models.ForeignKey(Message,related_name="comments",on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    

def create_message(MsgData,email):
    message=MsgData["message"]
    user=User.objects.get(email_address=email)
    new_message=Message.objects.create(message=message,user=user)
    return new_message

def get_all_messages():
    messages=Message.objects.all()
    return messages

def create_comment(CommentData,email):
    comment=CommentData['comment']
    user=User.objects.get(email_address=email)
    message=Message.objects.get(id=CommentData['msgid'])
    new_comment=Comment.objects.create(comment=comment,user=user,message=message)
    return new_comment

def delete_message(id):
    deleted_message=Message.objects.get(id=id)
    deleted_message.delete()

def get_time_difference():
    times= []
    messages=get_all_messages()
    current_time=datetime.now().strftime("%A, %B %d, %Y %H:%M:%S")
    time_converted=datetime.strptime(current_time,"%A, %B %d, %Y %H:%M:%S")

    for message in messages:
        message_time=message.created_at.strftime("%A, %B %d, %Y %H:%M:%S")
        time=datetime.strptime(message_time,"%A, %B %d, %Y %H:%M:%S")
        delta=time_converted-time
        time_difference_minutes=(delta.total_seconds()-(2*60*60))/60
        times.append(time_difference_minutes)
        print("delta",time_difference_minutes)
        print("message_time",message_time)
    print("Check time",current_time)
    print("list",times)

    return times