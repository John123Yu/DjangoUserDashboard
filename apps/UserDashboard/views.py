from django.shortcuts import render, HttpResponse, redirect
from models import Messages, Comments
from ..LoginAndReg.models import User, LoginManager, RegisterManager
from django.core.urlresolvers import reverse
from django.db.models import Count 

def index(request):
	context = {
	    'users' : User.registerMgr.all(),
	    'activeUser': User.registerMgr.get(id = request.session['login'])
	}
	return render(request, 'UserDashboard/index.html', context)

def createDisplay(request):
	return render(request, 'UserDashBoard/newUser.html')

def editProfileDisplay(request):
	user = User.registerMgr.get(id = request.session['login'])
	context = {
		'User': user
	}
	return render(request, 'UserDashboard/editProfile.html',  context )

def adminEdit(request, id):
	user = User.registerMgr.get(id = id)
	context = {
		'User': user
	}
	return render(request, 'UserDashboard/adminEdit.html', context )


def showWall(request, id):
	messages = Messages.objects.filter(reciever_id = id).order_by('id')
	request.session['reciever'] = id
	comments = Comments.objects.all()
	context = {
		'all_messages': messages,
		'all_comments': comments,
		'user': User.registerMgr.get(id = id)
	}
	return render(request, 'UserDashboard/showWall.html',  context )

def postMessage(request):
	newMessage = Messages.objects.create(message = request.POST['message'], user_id = request.session['login'], reciever_id = request.session['reciever'] )
	url = "/UserDashboard/showWall/" + str(request.session['reciever'])
	return redirect(url)

def deleteMessage(request, id):
	Messages.objects.get(id = id).delete()
	url = "/UserDashboard/showWall/" + str(request.session['reciever'])
	return redirect(url)

def postComment(request, id):
	newComment = Comments.objects.create(comment = request.POST['comment'], user_id = request.session['login'], message_id = id)
	url = "/UserDashboard/showWall/" + str(request.session['reciever'])
	return redirect(url)

def deleteComment(request, id):
	Comments.objects.get(id = id).delete()
	url = "/UserDashboard/showWall/" + str(request.session['reciever'])
	return redirect(url)

def logout(request):
	request.session['login'] = 0
	request.session['reciever'] = 0
	return redirect(reverse('login:index'))


