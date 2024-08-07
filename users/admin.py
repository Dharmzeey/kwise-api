from django.contrib import admin
from . import models

admin.site.register(models.State) 
admin.site.register(models.LGA) 
admin.site.register(models.User)
admin.site.register(models.EmailVerification)
admin.site.register(models.PhoneVerification)
admin.site.register(models.ForgotPassword)
admin.site.register(models.UserInfo)
admin.site.register(models.UserAddress)
