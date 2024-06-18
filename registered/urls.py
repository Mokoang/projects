
from django.contrib import admin
from django.urls import path,re_path
from . import views
# from  .views import TotalProductSales
urlpatterns = [
    #path('', views.dashboard, name ="dashboard"),
    #path('dash/', views.index, name ="index"),
    #path('path-to-report/', TotalProductSales.as_view()),
    #path('savedata/', views.savedata,name="savedata"),
    #path('details/', views.details, name="details"),
    path('lease_details/<int:lease_id>/', views.lease_detailz, name='lease_detailz'),
    path('lease_information/<int:lease_id>/', views.lease_information, name='lease_information'),
    path('lease_details/<int:lease_id>/save-data/', views.save_data, name='save_data'),
    path('lease_details/<int:lease_id>/get-data/', views.get_data, name='get_data'),
    path('lease/<int:pk>/details/', views.leasedetails, name='registered_lease_leasedetails'),

]
