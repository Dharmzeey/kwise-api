from django.urls import path
from . import views

app_name = "cart"
urlpatterns = [
  path("", views.get_cart, name="get_cart"),
  path("modify/", views.modify_cart, name="modify_cart"),
  path('checkout/', views.check_out, name="check_out"),
]