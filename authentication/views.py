import random
import pytz
from datetime import datetime
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.db import IntegrityError
from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, EmailVerification, PhoneVerification, ForgotPassword
from authentication.backends import EmailOrPhoneBackend

from utilities.error_handler import render_errors


from . import serializers as CustomSerializers


class UserCreateView(APIView):
  serializer_class = CustomSerializers.UserSerializer
  def post(self, request):
    serializer = self.serializer_class(data=request.data)
    if serializer.is_valid():
      try:
        user = serializer.save()
        tokens = TokenObtainPairSerializer().validate(request.data)
        access_token = tokens['access']
        # refresh_token = tokens['refresh']
        data = {
          'token': access_token,
          # 'refresh_token': refresh_token,
        }
        login(request, user, backend="authentication.backends.EmailOrPhoneBackend")
        # login(request, user)
        return Response(data, status=status.HTTP_201_CREATED)
      except IntegrityError:
        return Response({'error': 'User with this email or Phone Number already exists.'}, status=status.HTTP_409_CONFLICT)
    data = {"errors": render_errors(serializer.errors)}
    return Response(data, status=status.HTTP_400_BAD_REQUEST)
user_create = UserCreateView.as_view()


class UserLoginView(APIView):
  serializer_class = CustomSerializers.UserLoginSerializer
  def post(self, request):
    serializer = self.serializer_class(data=request.data)
    if serializer.is_valid():
      email = serializer.data.get("email", None)
      phone_number = serializer.data.get("phone_number", None)
      password = serializer.data.get("password")
      try:
        user = User.objects.get(email=email) if email is not None else User.objects.get(phone_number=phone_number)
      except User.DoesNotExist:
        return Response({"error": "User does not exists"}, status=status.HTTP_404_NOT_FOUND)
      email_authentication = authenticate(request=request, email=email, password=password)
      phone_authentication = authenticate(request=request, phone_number=phone_number, password=password)
      user = email_authentication if email_authentication is not None else phone_authentication
      if user is not None:
        login(request, user, backend="authentication.backends.EmailOrPhoneBackend")
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)  
        data = {
          "token": access_token
        }
        return Response(data, status=status.HTTP_200_OK)
      return Response({"error": "Invalid Credentials",}, status=status.HTTP_401_UNAUTHORIZED)
    data = {"errors": render_errors(serializer.errors)}
    return Response(data, status=status.HTTP_400_BAD_REQUEST)
user_login = UserLoginView.as_view()


class SendEmailVerificationView(APIView):
  permission_classes = [IsAuthenticated]
  def post(self, request):
    user = request.user
    if user.email_verified:
      return Response({"error": "Email has already been verified"}, status=status.HTTP_401_UNAUTHORIZED)
    try:
      EmailVerification.objects.get(user=user)
      return Response({"message": "Email Verification already sent"}, status=status.HTTP_409_CONFLICT)
    except EmailVerification.DoesNotExist:
      pin = str(random.randint(100000, 999999))
      # send email succesfully before saving to DB
      send_mail(
        'Kwiseworld Email Verification',
        f'Hello 👋.\nYour verification PIN is {pin}. \nIt will expire in 10 minutes',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
      )
      EmailVerification.objects.create(user=user, email=user.email, email_verification_pin=pin)
    return Response({"message": "verification PIN sent to email."}, status=status.HTTP_200_OK)
send_email_verificiation = SendEmailVerificationView.as_view()


class VerifyEmailView(APIView):
  permission_classes = [IsAuthenticated]
  serializer_class = CustomSerializers.EmailVeriificationSerializer
  def post(self, request):
    serializer = self.serializer_class(data=request.data)
    if serializer.is_valid():
      user=request.user
      try:
        fetch_pin = EmailVerification.objects.get(user=user)
      except EmailVerification.DoesNotExist:
        return Response({"error": "PIN has not been sent"}, status=status.HTTP_404_NOT_FOUND)
      utc=pytz.UTC
      if fetch_pin.expiry < utc.localize(datetime.now()):
        fetch_pin.delete() # remove the instnace on the Email OTP table if expired
        return Response({"error": "PIN expired"}, status=status.HTTP_401_UNAUTHORIZED)
      if fetch_pin.email_verification_pin == serializer.data['pin']:
        user.email_verified = True
        user.save()
        fetch_pin.delete() # remove the instnace on the Email OTP table 
        return Response({"message": "Email verified successfully"}, status=status.HTTP_200_OK)
      return Response({"error": "Invalid PIN"}, status=status.HTTP_403_FORBIDDEN)
    return Response({"errors": render_errors(serializer.errors)}, status=status.HTTP_404_NOT_FOUND)
verify_email = VerifyEmailView.as_view()


class SendPhoneVerificationView(APIView):
  def post(self, request):
    return Response()


class VerifyPhoneView(APIView):
  def post(self, request):
    return Response()
verify_phone = VerifyPhoneView.as_view()


class ForgotPasswordView(APIView):
  def post(self, request):
    serializer_class = CustomSerializers.ForgotPasswordSerializer
    serializer = serializer_class(data=request.data)
    if serializer.is_valid():
      try:
        user = User.objects.get(email=serializer.data['email'], phone_number=serializer.data['phone_number'])
        if ForgotPassword.objects.filter(user=user).exists(): # checks if the password PIN has been sent 
          return Response({"error": "password reset PIN already sent"}, status=status.HTTP_409_CONFLICT)
        pin = str(random.randint(100000, 999999))
        # send email succesfully before saving to DB
        send_mail(
          'Kwiseworld password reset',
          f'Hello 👋\nYour password reset PIN is {pin}. \nIt will expire in 10 minutes',
          settings.DEFAULT_FROM_EMAIL,
          [user.email],
          fail_silently=False,
        )
        ForgotPassword.objects.create(user=user, email=user.email, reset_password_pin=pin)
        return Response({"message": "password reset PIN sent to email."}, status=status.HTTP_200_OK)
      except User.DoesNotExist:
        return Response({"error": "User information not found"}, status=status.HTTP_404_NOT_FOUND)
    return Response({"errors": render_errors(serializer.errors)}, status=status.HTTP_404_NOT_FOUND)
forgot_password = ForgotPasswordView.as_view()


class ResetPasswordView(APIView):
  serializer_class = CustomSerializers.ResetPasswordSerializer
  def post(self, request):
    serializer = self.serializer_class(data=request.data)
    if serializer.is_valid():
      try:
        user = User.objects.get(email=serializer.data['email'], phone_number=serializer.data['phone_number'])
        fetch_pin = ForgotPassword.objects.get(user=user)
      except ForgotPassword.DoesNotExist:
        return Response({"error": "password reset PIN has not been sent"}, status=status.HTTP_404_NOT_FOUND)
      except User.DoesNotExist:
        return Response({"error": "User information not found"}, status=status.HTTP_404_NOT_FOUND)
      utc=pytz.UTC
      if fetch_pin.expiry < utc.localize(datetime.now()):
        fetch_pin.delete() # remove the instnace on the Email OTP table if expired
        return Response({"error": "password reset PIN expired"}, status=status.HTTP_401_UNAUTHORIZED)
      if fetch_pin.reset_password_pin == serializer.data['pin']:
        return Response({"message": "password reset PIN verified successfully"}, status=status.HTTP_200_OK) # after this, the next page to be shown to the user is where the user will fill in their new password
      return Response({"error": "Invalid PIN"}, status=status.HTTP_403_FORBIDDEN)
    return Response({"errors": render_errors(serializer.errors)}, status=status.HTTP_404_NOT_FOUND)
reset_password = ResetPasswordView.as_view()


class CreateNewPasswordView(APIView):
  serializer_class = CustomSerializers.CreateNewPasswordSerializer
  def post(self, request):
    serializer = self.serializer_class(data=request.data)
    if serializer.is_valid():
      try:
        user = User.objects.get(email=serializer.data['email'], phone_number=serializer.data['phone_number'])
        try:
          fetch_pin = ForgotPassword.objects.get(user=user, email=serializer.data['email'], reset_password_pin=serializer.data['pin'])
        except ForgotPassword.DoesNotExist:
          return Response({"error": "Could not reset password as PIN is invalid or User info invalid"}, status=status.HTTP_403_FORBIDDEN)
        user.set_password(serializer.data['password'])
        user.save()
        fetch_pin.delete()
      except User.DoesNotExist:
        return Response({"error": "User information not found"}, status=status.HTTP_404_NOT_FOUND)
      return Response({"message": "password changed successfully"}, status=status.HTTP_200_OK) 
    return Response({"errors": render_errors(serializer.errors)}, status=status.HTTP_404_NOT_FOUND)
create_new_password = CreateNewPasswordView.as_view()