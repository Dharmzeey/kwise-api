import uuid
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, AbstractBaseUser
from django.utils import timezone
from datetime import datetime, timedelta

class State(models.Model):
  name = models.CharField(max_length=20)  
  def __str__(self):
    return self.name
  
  class Meta:
    ordering = ["name"]
      

class LGA(models.Model):
  state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
  name = models.CharField(max_length=20)  
  def __str__(self):
    return self.name
  
  class Meta:
    ordering = ["name"]
  
  
class UserManager(BaseUserManager):
    def create_user(self, email, phone_no, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
          email=self.normalize_email(email),
          phone_no=phone_no
           
        )

        if password:
            user.set_password(password)
            user.save(using=self._db)
        else:
            user.set_unusable_password()

        return user

    def create_superuser(self, email, phone_no ,password=None):

        # extra_fields = {"is_staff": True, "is_superuser": True}

        user = self.create_user(
        email=self.normalize_email(email), phone_no=phone_no, password=password,
      )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)

        return user


def now_plus_10():
  """
  Function that returns current datetime + 10 minutes.
  """
  return datetime.now() + timedelta(minutes=10)

class User(AbstractBaseUser):
  id = models.UUIDField(editable=False, default=uuid.uuid4, unique=True, primary_key=True)
  password = models.CharField(max_length=128)
  phone_no = models.CharField(max_length=11, validators=[RegexValidator(r'^0\d{10}$', 'Mobile number should be 11 digits starting with 0.')])
  email = models.EmailField(max_length=100 ,unique=True)
  email_verified = models.BooleanField(default=False)
  phone_no_verified = models.BooleanField(default=False)
  
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  
  # required fields
  date_joined = models.DateTimeField(auto_now_add=True)
  last_login = models.DateTimeField(auto_now=True)
  is_admin = models.BooleanField(default=False)
  is_staff = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)
  is_superuser = models.BooleanField(default=False)
  
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['phone_no']
  objects = UserManager()
  
  class Meta:
    ordering = ["date_joined"]
    
  def __str__(self):
    return self.email
  
  def has_perm(self, perm, obj=None):
    return self.is_admin
  
  def has_module_perms(self, app_label):
    return True
  

class EmailVerification(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_email_verification")
  email = models.EmailField()
  email_verification_pin = models.CharField(max_length=6, blank=True, null=True)
  expiry = models.DateTimeField(default=now_plus_10)
  

class PhoneVerification(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_verify_phone")
  phone = models.CharField(max_length=11, validators=[RegexValidator(r'^0\d{10}$', 'Mobile number should be 11 digits starting with 0.')])
  phone_verification_pin = models.CharField(max_length=6, blank=True, null=True)
  expiry = models.DateTimeField(default=now_plus_10)


class ForgotPassword(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_forgot_password")
  email = models.EmailField()
  reset_password_pin = models.CharField(max_length=6, blank=True, null=True)
  expiry = models.DateTimeField(default=now_plus_10)
  

class UserInfo(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_info")
  first_name = models.CharField(max_length=150, null=False)
  last_name = models.CharField(max_length=150, null=False)
  other_name = models.CharField(max_length=100, blank=True, null=True)
  alternate_email = models.EmailField(unique=True)
  address = models.CharField(max_length=255)
  alternate_phone_no = models.CharField(max_length=11, validators=[RegexValidator(r'^0\d{10}$', 'Mobile number should be 11 digits starting with 0.')])

  def __str__(self):
    return self.user.username


class UserAddress(models.Model):
  state = models.ForeignKey(State, on_delete=models.SET_NULL, related_name="user_state", null=True)
  city_town = models.CharField(max_length=30)
  lga = models.ForeignKey(LGA, on_delete=models.SET_NULL, related_name="user_lga", null=True)
  prominent_motor_park = models.CharField(max_length=50, null=True, blank=True)
  landmark_signatory_place = models.CharField(max_length=50, null=True, blank=True)
  address = models.CharField(max_length=200)
  def __str__(self):
    return f"{self.user.username} - {self.address}"
