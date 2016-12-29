from django.shortcuts import render, HttpResponse, redirect
from models import User
from django.contrib import messages
from django.core.urlresolvers import reverse

# Create your views here.
def index(request):
    return render (request, 'LoginAndReg/index.html')

def register(request):
	error_messages = {}
	if request.method == "POST":
		result = User.registerMgr.userRegister(request.POST['first_name'], request.POST['last_name'], request.POST['email'], request.POST['password'], request.POST['confirm_password'], request.POST['birthday'], 0, False)
		if result[0]:
			user = result[1]
			request.session['login'] = result[1].id
			if result[1].id == 7:
				user.user_level = "Admin"
				user.save()
			else:
				user.user_level = "Normal"
				user.save()
			return redirect(reverse('UserDashboard:index'))
		else:
			error_messages = result[1]
			return render(request, 'LoginAndReg/index.html',  error_messages )
	else:
		pass

def login(request):
	error_messages = {}
	if request.method == "POST":
		result = User.loginMgr.login(request.POST['email'], request.POST['password'])
		if result[0]:
			user = User.loginMgr.get(email = request.POST['email'])
			request.session['login'] = user.id
			# messages.info(request, 'Three Credits remain')
			# messages.error(request, "Entered BLA BLA BLA")
			print request.session['login']
			return redirect(reverse('UserDashboard:index'))
		else:
			error_messages = result[1]
			return render(request, 'LoginAndReg/index.html',  error_messages )
	else:
		return redirect ('/')

def updateInfo(request, id):
	error_messages = {}
	user = User.registerMgr.get(id = request.session['login'])
	if id == str(0):
		result = User.registerMgr.userRegister(request.POST['first_name'], request.POST['last_name'], request.POST['email'], user.password, user.password, request.POST['birthday'], request.session['login'], False)
	else:
		result = User.registerMgr.userRegister(request.POST['first_name'], request.POST['last_name'], request.POST['email'], user.password, user.password, request.POST['birthday'], id, False)
	if result[0]:
		return redirect(reverse('UserDashboard:index'))
	elif result[0] == False and id == str(0):
	    error_messages = result[1]
	    return render(request, 'UserDashboard/editProfile.html',  error_messages )
	elif result[0] == False and id > 0:
		error_messages = result[1]
		user = User.registerMgr.get(id = id)
		context = {
			'User': user,
			'error_messages': error_messages
		}
		print context['error_messages']
	return render(request, 'UserDashboard/adminEdit.html', context)

def updatePassword(request, id):
	error_messages = {}
	user = User.registerMgr.get(id = request.session['login'])
	if id == str(0):
		result = User.registerMgr.userRegister(user.firstName, user.lastName, user.email, request.POST['password'], request.POST['confirm_password'], user.birthday, request.session['login'], True)
	else:
		result = User.registerMgr.userRegister(user.firstName, user.lastName, user.email, request.POST['password'], request.POST['confirm_password'], user.birthday, id, True)
	if result[0]:
		return redirect(reverse('UserDashboard:index'))
	elif result[0] == False and id == str(0):
		error_messages = result[1]
		return render(request, 'UserDashboard/editProfile.html',  error_messages )
	elif result[0] == False and id > 0:
		error_messages = result[1]
		user = User.registerMgr.get(id = id)
		context = {
			'User': user,
			'error_messages': error_messages
		}
		print context['error_messages']
	return render(request, 'UserDashboard/adminEdit.html', context)
		# url = "/UserDashboard/users/edit/" + str(id)
		# return redirect(url)

def updateDescription(request):
	user = User.registerMgr.get(id = request.session['login'])
	user.profileInformation = request.POST['description']
	user.save()
	return redirect(reverse('UserDashboard:index'))

def removeUser(request, id):
	User.registerMgr.get(id = id).delete()
	return redirect(reverse('UserDashboard:index'))

def createUser(request):
	error_messages = {}
	if request.method == "POST":
		result = User.registerMgr.userRegister(request.POST['first_name'], request.POST['last_name'], request.POST['email'], request.POST['password'], request.POST['confirm_password'], request.POST['birthday'], 0, False)
		if result[0]:
			user = result[1]
			user.user_level = "Normal"
			user.save()
			return redirect(reverse('UserDashboard:index'))
		else:
			error_messages = result[1]
			return render(request, 'UserDashboard/newUser.html',  error_messages )
	else:
		pass
