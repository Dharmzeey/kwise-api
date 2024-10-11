from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = "authentication"
urlpatterns = [
  
  path('', views.user_create, name="user_create"),
  path('login/', views.user_login, name="user_login"),
  
  path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
  
  path('email-verification/', views.send_email_verificiation, name="send_email_verificiation"),
  path('email-verification/confirm/', views.verify_email, name="verify_email"),
  path('password/forgot/', views.request_password_reset, name="forgot_password"),
  path('password/reset/', views.verify_password_reset_pin, name="reset_password"),
  path('password/new/', views.create_new_password, name="create_new_password"),
  
  path('logout/', views.logout, name="logout"),
]