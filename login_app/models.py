from django.db import models
import re
from datetime import datetime,date
import bcrypt

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['firstname']) < 2:
            errors["firstname"] = "First Name should be at least 2 characters"
        if len(postData['lastname']) < 2:
            errors["lastname"] = "Last Name should be at least 2 characters"
        if postData['password'] !=postData['confirm_pw']:
            errors["password"] = "Password doesn't match"
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['emailaddress']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"
        if User.objects.filter(email_address = postData['emailaddress']).exists():
            errors['email'] = "This email address is already registered"
        if postData['birthday']:
            birthdate=postData['birthday']
            current_date=datetime.now().strftime("%Y-%m-%d")
            age=get_age(birthdate)
            if age <13:
                errors["age"] = "Age should be more than 13"
            if birthdate > current_date:
                errors["birthday"] = "Birthday should be in the past"
        return errors

    def login_validator(self,postData):
        errors= {}
        if not User.objects.filter(email_address = postData['emailaddress']).exists():
            errors["login"]="email address or password incorrect"
        else:
            user=User.objects.filter(email_address = postData['emailaddress'])
            logged_user=user[0]
            if bcrypt.checkpw(postData['password'].encode(), logged_user.password.encode()):
                print("password match")
            else:
                errors["login"]="email address or password incorrect"
                print("failed password")
        return errors

class User(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email_address=models.CharField(max_length=255)
    birthday=models.DateField(null=True)
    password= models.CharField(max_length=255,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects = UserManager()

def create_user(userdata):

    password = userdata['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    password=pw_hash
    firstname=userdata['firstname']
    lastname=userdata['lastname']
    emailaddress=userdata['emailaddress']
    birthday=userdata['birthday']
    new_user=User.objects.create(first_name=firstname,last_name=lastname,email_address=emailaddress,
    password=password, birthday=birthday)
    
    return new_user

def get_age(birthdate):
    formatter_string = "%Y-%m-%d"
    new_birthday = datetime.strptime(birthdate, formatter_string)
    today = date.today()
    print("*****************************")
    print(type(today))
    print(type(new_birthday))
    print(today.year)
    print(new_birthday.year)
    age = today.year - new_birthday.year
    print(age)
    print("*****************************")

    return age
