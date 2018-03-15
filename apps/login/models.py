#####################################################
from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
from datetime import datetime
################### email regex #################################
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
############# name regex ############################################
NAME_REGEX = re.compile(r'^[A-Za-z]\w+$')
##############################################################   
class UserManager(models.Manager):
    def validate_and_register(self, postData):
        errors = {}
       ##############   NAME   ###############################
        if not len(postData['name']):
            errors['name'] = "field is empty."
        elif len(postData['name']) < 2:
            errors['name'] = "Name too short."
        #########   Alias ###################################
        if not len(postData['alias']):
            errors['alias'] = "field is empty."
        elif len(postData['alias']) < 2:
            errors['alias'] = "Alias too short."
        ############### email validations #####################
        if not len(postData['userName']):
            errors['userName'] = "field is empty."
        elif len(postData['alias']) < 2:
            errors['userName'] = "UserName too short."
        #################### email validations ##################
        if not len(postData['email']):
            errors['email'] = "Email field can not be empty."
        elif not re.match(EMAIL_REGEX, postData['email']):
            errors['email'] = "Invalid email! Please input the right format of an email like: user@mail.com"
        ###################  password ######################
        if not len(postData['password']):
            errors['password'] = "Password field can not be empty."
        elif len(postData['password']) < 8:
            errors['password'] = "Password too short. Input at least 8 characters"
        elif postData['password'] != postData['confirm_pass']:
            errors['confirm_pass'] = "Password not confirmed. Please pay more attention"
        ###################### birthday and date #################
        if not postData['datehired']:
            errors['datehired'] = "field is empty"
        else:
            now = datetime.today().date()
            #birthday = datetime.strptime(postData['birthday'], "%A %d. %B %Y").date()
            datehired = datetime.strptime(postData['datehired'], "%Y-%m-%d").date()
           
        if len(errors):
            return (False, errors)
        else:
            password = postData['password'].encode()
            hashed = bcrypt.hashpw(password, bcrypt.gensalt())
            self.create(name = postData['name'], alias = postData['alias'], email = postData['email'], password = hashed, datehired = datehired)
            ####################
            new_user = self.create(
                name=postData['name'],
                alias=postData['alias'],
                email=postData['email'],
                password=hashed,
                datehired=postData['datehired']
            )
            #print new_user
            return (True,new_user)
            

    def validate_and_login(self, postData):
        errors_login = {}
        # Email Validation when Login
        if not len(postData['email']):
            errors_login['login_email_error'] = "Please provide an email."
        else:
            if not self.filter(email = postData['email']):
                errors_login['login_error'] = "wrong email or passwd."
        
        if not len(errors_login):
            user = self.filter(email = postData['email'])
        # Password Validation when Login
            if not len(postData['password']):
                errors_login['login_password_error'] = "Please type your email password."
            else:
                password = postData['password'].encode()
                hashed = self.filter(email = postData['email'])[0].password.encode()
                if not bcrypt.checkpw(password, hashed):
                    errors_login['login_error'] = "wrong email or passwd"

        if len(errors_login):
            return (False, errors_login)
        else:
            return (True, self.filter(email = postData['email']))
      
        if len(errors_login):
            return (False, errors_login)
        else:
            return (True, self.filter(email = postData['email']))
              
####################  Model ######################################
class User(models.Model):
    name = models.CharField(max_length = 255)
    alias = models.CharField(max_length = 45)
    email = models.CharField(max_length = 255)
    userName = models.CharField(max_length=48)
    password = models.CharField(max_length = 255)
    datehired = models.DateField(max_length = 45)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

