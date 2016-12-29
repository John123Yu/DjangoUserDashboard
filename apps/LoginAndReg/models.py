from __future__ import unicode_literals
from django.db import models
import re
from datetime import datetime
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
PASSWORD_REGEX = re.compile(r'^(?=.*[A-Z])(?=.*\d)')

class RegisterManager(models.Manager):
    def userRegister(self, firstName, lastName, email, password, confirmPassword, birthday, session, changePassword):
		errors = {}
		try:
			birthday_object = datetime.strptime(birthday, '%Y-%m-%d')
		except:
			if changePassword == False:
				errors['BirthdayError'] = "Birthday not in correct format"
			birthday_object = datetime.today()
		try:
			user = User.registerMgr.get(email = email)
		except:
			user = 0
		if len(email) == 0:
		    errors['EmailRequired'] = ("Email is required")
		elif not EMAIL_REGEX.match(email):
		    errors['InvalidEmail'] = ("Invalid Email")
		if user != 0 and session == 0:
			errors['EmailDuplicate'] = "Email Already In Use!"
		if len(firstName) < 2 or len(lastName) < 2:
			errors['TwoCharacters'] = ("First name and last name must be at least two characters")
		if firstName.isalpha() == False or lastName.isalpha() == False:
			errors['IsAlpha'] = ("First and last name must contain only alphabetic characters")
		if len(password) < 1 or len(confirmPassword) < 1:
			errors['PasswordRequired'] = ("Password and confirm password is required")
		if len(password) < 8:
			errors['PasswordLength'] = ("Password needs to be at least 8 characters")
		if not PASSWORD_REGEX.match(password):
			errors['InvalidPassword'] = ("Password requires one uppercase letter and one number")
		if password != confirmPassword:
			errors['PasswordNonmatch'] = ("Confirm password must match password")
		if birthday_object >= datetime.today():
			errors['BirthdayPast'] = "Birthday must be in the past"
		if len(errors) is not 0:
			return (False, errors)
		elif len(errors) == 0 and session == 0:
			pw_bytes = password.encode('utf-8')
			hashed = bcrypt.hashpw(pw_bytes, bcrypt.gensalt())
			user = User.registerMgr.create(firstName = firstName, lastName = lastName, email=email, password = hashed, birthday = birthday)
			user.save()
			return (True, user)
		elif len(errors) == 0 and session > 0 and changePassword == False:
			User.registerMgr.filter(id = session).update(firstName = firstName, lastName = lastName, email = email, birthday = birthday, password = password)
			return (True, 1)
		elif len(errors) == 0 and  session > 0 and changePassword == True: 
			pw_bytes = password.encode('utf-8')
			hashed = bcrypt.hashpw(pw_bytes, bcrypt.gensalt())
			User.registerMgr.filter(id = session).update(password = hashed)
			return (True, 1)


class LoginManager(models.Manager):
	def login(self, email, password):
		errors = {}
		try:
			user = User.loginMgr.get(email = email)
		except:
			user = 0

		if user != 0:
			hashed = user.password.encode('utf-8')
			pw_bytes = password.encode('utf-8')
			if bcrypt.hashpw(pw_bytes, hashed) == hashed:
				a = 1
			else:
				errors["IncorrectLogin"] = "Incorrect Password"
		else:
			errors["NoEmail"] = "Entered Email Not in Database"
		if len(errors) is not 0:
			return (False, errors)
		else:
			return (True, 0)


class User(models.Model):
	firstName = models.CharField(max_length=100)
	lastName = models.CharField(max_length=100)
	email = models.CharField(max_length=100)
	user_level = models.CharField(max_length = 100, null = True)
	password = models.CharField(max_length=250)
	birthday = models.DateField(null = True)
	profileInformation = models.TextField(null = True)
	created_at = models.DateField(auto_now_add=True)
	updated_at = models.DateField(auto_now=True)
	registerMgr = RegisterManager()
	loginMgr = LoginManager()

