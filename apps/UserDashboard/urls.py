from django.conf.urls import url, include # Notice we added include
from . import views

urlpatterns = [
	url(r'^$', views.index, name = "index"),
	url(r'^users/new$', views.createDisplay, name = "createDisplay"),
	url(r'^users/edit$', views.editProfileDisplay, name = "editProfileDisplay"),
	url(r'^showWall/(?P<id>\d+)$', views.showWall, name = "showWall"),
	url(r'^postMessage$', views.postMessage, name = "postMessage"),
	url(r'^deleteMessage/(?P<id>\d+)$', views.deleteMessage, name = "deleteMessage"),
	url(r'^postComment/(?P<id>\d+)$', views.postComment, name = "postComment"),
	url(r'^deleteComment/(?P<id>\d+)$', views.deleteComment, name = "deleteComment"),
	url(r'^logout$', views.logout, name = "logout"),
	url(r'^users/edit/(?P<id>\d+)$', views.adminEdit, name = "adminEdit")
]