from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"), 
    path('create', views.create, name="create"),
    path('studio', views.studio, name="studio"),
    path('cstudio/<cid>', views.cstudio, name="cstudio"),
    path('video/<vid>', views.video, name="video"),
    path('vidlk', views.vidlk, name="vidlk"),
    path('vidcmt', views.vidcmt, name="vidcmt"),
    path('videdt', views.videdt, name="videdt"),
    path('viddelete', views.viddelete, name="viddelete"),
]