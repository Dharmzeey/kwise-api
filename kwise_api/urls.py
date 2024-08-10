from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('adedamola/', admin.site.urls),
    path('v1/base/', include('base.urls')),
    path('v1/authentication/', include('authentication.urls')),
    path('v1/users/', include('users.urls')),
    path('v1/products/', include('products.urls')),
]
