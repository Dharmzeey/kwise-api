from django.contrib import admin
from . import models

admin.site.register(models.User)
admin.site.register(models.EmailVerification)
admin.site.register(models.PhoneVerification)
admin.site.register(models.ForgotPassword)