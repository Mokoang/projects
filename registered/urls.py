
from django.contrib import admin
from django.urls import path,re_path
from . import views
from  .views import TotalProductSales

urlpatterns = [
    #path('', views.dashboard, name ="dashboard"),
    #path('dash/', views.index, name ="index"),
    #path('path-to-report/', TotalProductSales.as_view()),
    #path('savedata/', views.savedata,name="savedata"),
    #path('details/', views.details, name="details"),
]
