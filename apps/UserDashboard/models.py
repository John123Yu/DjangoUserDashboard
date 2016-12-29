from __future__ import unicode_literals
from django.db import models
from ..LoginAndReg.models import User, LoginManager, RegisterManager
# Create your models here.

class Messages(models.Model):
	message = models.TextField()
	user = models.ForeignKey(User, related_name = "poster")
	reciever = models.ForeignKey(User, related_name = "reciever", null = True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Comments(models.Model):
	comment = models.TextField()
	message = models.ForeignKey(Messages)
	user = models.ForeignKey(User)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)