from django.db import IntegrityError
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import DestroyAPIView, RetrieveAPIView


from . import serializers as CustomSerializers
from .models import UserInfo, UserAddress, State
from utils.error_handler import render_errors


class CreateUserInfoView(APIView):
  serializer_class = CustomSerializers.UserInfoSerializer
  permission_classes = [IsAuthenticated]
  
  def post(self, request):
    serializer = self.serializer_class(data=request.data)
    if not request.user.email_verified:
      return Response({"error": "Email not verified"}, status=status.HTTP_401_UNAUTHORIZED)
    if serializer.is_valid():
      try:
        serializer.save(user=request.user)
      except IntegrityError:
        data = {"error": "User profile already exists"}
        return Response(data, status=status.HTTP_409_CONFLICT)      
      data = {"message": "Profile created successfully", "data": serializer.data}
      return Response(data, status=status.HTTP_200_OK)
    data = {"errors": render_errors(serializer.errors)}
    return Response(data, status=status.HTTP_400_BAD_REQUEST)
add_user_info = CreateUserInfoView.as_view()


class RetrieveUserInfoView(APIView):
  serializer_class = CustomSerializers.UserInfoSerializer
  permission_classes = [IsAuthenticated]
  def get(self, request):
    user = request.user.user_info
    serializer = self.serializer_class(instance=user)
    data = {"message": "user details", "data": serializer.data}
    return Response(data, status=status.HTTP_200_OK)
retrieve_user_info = RetrieveUserInfoView.as_view()


class UpdateUserInfoView(APIView):
  serializer_class = CustomSerializers.UserInfoSerializer
  permission_classes = [IsAuthenticated]
  
  def patch(self, request):
    try:
      UserInfo.objects.get(user=request.user)
      user = request.user.user_info
    except UserInfo.DoesNotExist:
      return Response({"error": "Add your user information"}, status=status.HTTP_404_NOT_FOUND)
    serializer = self.serializer_class(instance=user, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      data = {"message": "Profile updated successfully", "data": serializer.data}
      return Response(data, status=status.HTTP_200_OK)
    data = {"errors": render_errors(serializer.errors)}
    return Response(data, status=status.HTTP_400_BAD_REQUEST)
update_user_info = UpdateUserInfoView.as_view()


class DeleteUserView(DestroyAPIView):
  serializer_class = CustomSerializers.UserInfoSerializer
  permission_classes = [IsAuthenticated]
  def get_object(self):
    user = self.request.user
    if not user.is_authenticated:
      raise PermissionDenied("User cannot be deleted")
    return user
delete_user = DeleteUserView.as_view()


def _check_lga_and_state_match(serializer):
  lga = serializer.validated_data.get("lga", None)
  state = serializer.validated_data.get("state", None)
  if state.id != lga.state.id:
    data = {"error": "The LGA passed does not belong to the state being sent"}
    return Response(data, status=status.HTTP_400_BAD_REQUEST)
  return None

class CreateUserAddressView(APIView):
  serializer_class = CustomSerializers.UserAddressSerializer
  permission_classes = [IsAuthenticated]

  def post(self, request):
    serializer = self.serializer_class(data=request.data)
    if not request.user.email_verified:
      return Response({"error": "Email not verified"}, status=status.HTTP_401_UNAUTHORIZED)
    if serializer.is_valid():
      validation_response = _check_lga_and_state_match(serializer)     
      if validation_response:
        return validation_response
      try:
        serializer.save(user=request.user)
      except IntegrityError:
        data = {"error": "User Address profile already exists"}
        return Response(data, status=status.HTTP_409_CONFLICT)
      data = {"message": "Address created successfully", "data": serializer.data}
      return Response(data, status=status.HTTP_201_CREATED)
    data = {"errors": render_errors(serializer.errors)}
    return Response(data, status=status.HTTP_400_BAD_REQUEST)
create_user_address = CreateUserAddressView.as_view()


class RetrieveUserAddressView(APIView):
  serializer_class = CustomSerializers.UserAddressSerializer
  permission_classes = [IsAuthenticated]
  def get(self, request):
    user = request.user.user_address
    serializer = self.serializer_class(instance=user)
    data = {"message": "user address information", "data": serializer.data}
    return Response(data, status=status.HTTP_200_OK)
retrieve_user_address = RetrieveUserAddressView.as_view()


class UpdateUserAddressView(APIView):
  serializer_class = CustomSerializers.UserAddressSerializer
  permission_classes = [IsAuthenticated]
  
  def patch(self, request):
    try:
      user = UserAddress.objects.get(user=request.user)
    except UserAddress.DoesNotExist:
      return Response({"error": "Add your user Address"}, status=status.HTTP_404_NOT_FOUND)
    serializer = self.serializer_class(instance=user, data=request.data, partial=True)
    if serializer.is_valid():
      validation_response = _check_lga_and_state_match(serializer)     
      if validation_response:
        return validation_response
      serializer.save()
      data = {"message": "Address updated successfully", "data": serializer.data}
      return Response(data, status=status.HTTP_200_OK)
    data = {"errors": render_errors(serializer.errors)}
    return Response(data, status=status.HTTP_400_BAD_REQUEST)
update_user_address = UpdateUserAddressView.as_view()
