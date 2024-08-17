from django.urls import path
from . import views

app_name = "cart"
urlpatterns = [
  path("", views.get_cart, name="get_cart"),
  path("modify/", views.modify_cart, name="modify_cart"),
  path("checkout/", views.checkout, name="checkout"),
  path("summary/", views.order_summary, name="order_summary"),
]