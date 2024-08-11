from rest_framework import serializers
from .models import UserInfo, UserAddress

  
class UserInfoSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserInfo
    fields = ["first_name", "last_name", "other_name", "alternate_email", "alternate_phone_number"]


class UserAddressSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserAddress
    fields = ["state", "city_town", "lga", "prominent_motor_park", "landmark_signatory_place", "address"]
    extra_kwargs = {
      "state": {"required": True},
      "city_town": {"required": True},
      "lga": {"required": True},
      "address": {"required": True},
    }
  def to_representation(self, instance):
    representation = super().to_representation(instance)
    representation['state'] = instance.state.name
    representation['lga'] = instance.lga.name
    return representation