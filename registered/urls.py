
from django.contrib import admin
from django.urls import path,re_path
from . import views


admin.site.site_header = 'Admininistrator'
    
urlpatterns = [
    path('', views.dashboard, name ="dashboard"),
    #path('registered/', views.registration, name ="registration"),
    #path('savedata/', views.savedata,name="savedata"),
    #path('details/', views.details, name="details"),
]
