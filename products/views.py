from rest_framework.generics import RetrieveAPIView, ListAPIView
from . import serializers as customSerializers
from .models import Product


class ProductListView(ListAPIView):
  serializer_class = customSerializers.ProductSerializer
  queryset = Product.objects.all()
product_list = ProductListView.as_view()


class ProductDetailView(RetrieveAPIView):
  queryset=Product.objects.all()
  serializer_class = customSerializers.ProductSerializer
  def get_object(self):
    uuid = self.kwargs.get('pk')
    return Product.objects.get(uuid=uuid)

product_detail = ProductDetailView.as_view()