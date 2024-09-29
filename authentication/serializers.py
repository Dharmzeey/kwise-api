import re
from rest_framework import serializers
from users.models import User


# USER RELATED SERIALIZERS
class UserSerializer(serializers.ModelSerializer):
  id = serializers.SerializerMethodField()
  password = serializers.CharField(min_length=8, max_length=150, write_only=True, error_messages={
    'required': 'Please enter a password',
    'min_length': 'Password must be at least 8 characters long',
    'max_length': 'Password must be no more than 128 characters long',
    'invalid': 'Please enter a valid password'
  })
  email = serializers.EmailField(min_length=4, max_length=150, error_messages={
    'required': 'Email Address cannot be empty',
    'invalid': 'Please enter a valid Email Address',
  })
  phone_number = serializers.CharField(min_length=11, max_length=13, error_messages={
    'required': 'Phone Number cannnot be empty',
    'invalid': 'Please enter a Phone Number',
  })
  
  
  class Meta:
    model = User
    fields = ['id', 'email', 'phone_number', 'password']
      
  def create(self, validated_data):
    password = validated_data.pop("password")
    user = super().create(validated_data)
    user.set_password(password)
    user.save()
    return user
  
  def get_id(self, obj):
    return obj.uuid
  

class UserLoginSerializer(serializers.Serializer):
  password = serializers.CharField(min_length=8, max_length=150, error_messages={
    'required': 'Please enter a password',
    'min_length': 'Password must be at least 8 characters long',
    'max_length': 'Password must be no more than 128 characters long',
    'invalid': 'Please enter a valid password'
  })
  email = serializers.CharField(min_length=4, max_length=150, required=False, error_messages={
    'required': 'Please enter an Email Address',
    'invalid': 'Please enter a valid Email Address',
  })
  phone_number = serializers.CharField(min_length=11, max_length=13, required=False,)
  


class EmailVeriificationSerializer(serializers.Serializer):
  email_pin = serializers.CharField(min_length=6, max_length=6)
  

class ForgotPasswordSerializer(serializers.Serializer):
  phone_number = serializers.CharField()
  email = serializers.EmailField()
  
  
class ResetPasswordSerializer(serializers.Serializer):
  phone_number = serializers.CharField()
  email = serializers.EmailField()
  pin = serializers.CharField(min_length=6, max_length=6)
  

class CreateNewPasswordSerializer(serializers.Serializer):
  phone_number = serializers.CharField()
  email = serializers.EmailField()
  pin = serializers.CharField(min_length=6, max_length=6)
  password = serializers.CharField(min_length=8, max_length=150, error_messages={
    'required': 'Please enter a password',
    'min_length': 'Password must be at least 8 characters long',
    'max_length': 'Password must be no more than 128 characters long',
    'invalid': 'Please enter a valid password'
  })  
