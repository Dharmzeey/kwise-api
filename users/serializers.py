from rest_framework import serializers

from products.models import Product
from products.serializers import ProductSerializer

from .models import UserInfo, UserAddress, PendingOrder, CompletedOrder, Favorite

  
class UserInfoSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserInfo
		fields = ["first_name", "last_name", "other_name", "alternative_email", "alternative_phone_number"]


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
	

class PendingOrderSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = PendingOrder
		exclude = ["id", "user"]
	def to_representation(self, instance):
		representation = super().to_representation(instance)
		representation['state'] = instance.state.name
		representation['lga'] = instance.lga.name
		representation['product'] = instance.product.uuid
		return representation
	
    
class CompletedOrderSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = CompletedOrder
		exclude = ["id", "user"]
	def to_representation(self, instance):
		representation = super().to_representation(instance)
		representation['product'] = instance.product.uuid
		return representation
    
    
class FavoriteSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.CharField(write_only=True)

    class Meta:
        model = Favorite
        fields = ['product', 'product_id']
        read_only_fields = ['product']

    def create(self, validated_data):
        request = self.context.get('request')
        product_uuid = validated_data.pop('product_id')
        product = Product.objects.get(uuid=product_uuid)
        favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
        return favorite
    