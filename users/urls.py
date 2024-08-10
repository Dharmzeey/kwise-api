from django.urls import path
from . import views

app_name = "users"
urlpatterns = [  
  path('info/', views.add_user_info, name="add_user_info"),
  path('info/retrieve/', views.retrieve_user_info, name="retrieve_user_info"),
  path('info/update/', views.update_user_info, name="update_user_info"),
  path('delete/', views.delete_user, name="delete_user_info"), 
  
  path('address/', views.create_user_address, name="create_user_address"),
  path('address/retrieve/', views.retrieve_user_address, name="retrieve_user_address"),
  path('address/update/', views.update_user_address, name="update_user_address"),

]

