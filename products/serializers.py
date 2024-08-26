from rest_framework import serializers
from .models import Category, Brand, Product


class CategorySerializer(serializers.ModelSerializer):
  class Meta:
    model = Category
    fields = "__all__"
    
    
class BrandSerializer(serializers.ModelSerializer):
  class Meta:
    model = Brand
    fields = "__all__"
  def to_representation(self, instance):
    representation = super().to_representation(instance)
    representation['category'] = instance.category.name
    return representation

class ProductSerializer(serializers.ModelSerializer):
  availabilityStatus = serializers.SerializerMethodField()
  utilizationStatus = serializers.SerializerMethodField()
  id = serializers.SerializerMethodField()
    
  class Meta:
    model = Product
    exclude = ["uuid", "utilization_status", "availability_status"]
    
  def to_representation(self, instance):
    representation = super().to_representation(instance)
    representation["category"] = instance.category.name 
    representation["brand"] = instance.brand.name
    return representation
  
  def get_availabilityStatus(self, obj):
    return obj.get_availability_status_display()

  def get_utilizationStatus(self, obj):
    return obj.get_utilization_status_display()
  
  # This below will take the uuid from the database and render it as ID (the DB has id as pk but uuid as the external exposed id for querying sake alone)
  def get_id(self, obj):
    return str(obj.uuid)