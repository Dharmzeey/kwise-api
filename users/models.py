from django.core.validators import RegexValidator
from django.db import models
from authentication.models import User
from base.models import State, LGA


class UserInfo(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_info")
  first_name = models.CharField(max_length=150, null=False)
  last_name = models.CharField(max_length=150, null=False)
  other_name = models.CharField(max_length=100, blank=True, null=True)
  alternate_email = models.EmailField(null=True, blank=True)
  alternate_phone_number = models.CharField(max_length=11, validators=[RegexValidator(r'^0\d{10}$', 'Mobile number should be 11 digits starting with 0.')])

  def __str__(self):
    return f"{self.first_name} - {self.last_name}"


class UserAddress(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_address")
  state = models.ForeignKey(State, on_delete=models.SET_NULL, related_name="user_state", null=True)
  city_town = models.CharField(max_length=30)
  lga = models.ForeignKey(LGA, on_delete=models.SET_NULL, related_name="user_lga", null=True)
  prominent_motor_park = models.CharField(max_length=50, null=True, blank=True)
  landmark_signatory_place = models.CharField(max_length=50, null=True, blank=True)
  address = models.TextField()
  def __str__(self):
    return f"{self.user} - {self.address}"
