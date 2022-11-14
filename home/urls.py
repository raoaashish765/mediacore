from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    path('activate/<uidb64>/<token>', views.activate, name="activate"),
    path('usersettings', views.usersettings, name="usersettings"),
    path('user', views.userr, name="userr"),
    path('user/<name>', views.user, name="user"),
    path('followview', views.followview, name="followview"),
    path('user/<name>/following', views.fing, name="fing"),
    path('user/<name>/followers', views.fers, name="fers"),
    path('posts', views.posts, name="posts"),
    path('postview/<pid>', views.postview, name="postview"),
    path('postdelete', views.postdelete, name="postdelete"),
    path('likepst/<lk>', views.likepst, name="likepst"),
    path('cmntpst', views.cmntpst, name="cmntpst"),
    path('report', views.report, name="report"),
    path('srch', views.srch, name="srch"),
]