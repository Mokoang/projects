
from django.contrib import admin
from django.urls import path,re_path
from . import views

urlpatterns = [
    #path('', views.dashboard, name ="dashboard"),
    path('dash/', views.index, name ="index"),
    #path('savedata/', views.savedata,name="savedata"),
    #path('details/', views.details, name="details"),
]
