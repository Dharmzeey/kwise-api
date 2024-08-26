from django.http import Http404
from rest_framework.generics import RetrieveAPIView, ListAPIView
from . import serializers as customSerializers
from .models import Product, Category, Brand
from rest_framework.response import Response
from rest_framework import status


class ProductCategoryView(ListAPIView):
  serializer_class = customSerializers.CategorySerializer
  queryset = Category.objects.all()
  
product_categories = ProductCategoryView.as_view()


class ProductBrandView(ListAPIView):
  serializer_class = customSerializers.BrandSerializer
  
  def get_queryset(self):
    q = self.request.query_params.get("q")
    print(q)
    qs = Brand.objects.filter(category__name__iexact=q)
    print(qs)
    return qs
  
product_brands = ProductBrandView.as_view()


class ProductListView(ListAPIView):
  serializer_class = customSerializers.ProductSerializer
  queryset = Product.objects.all()
  
product_list = ProductListView.as_view()


class ProductSearchView(ListAPIView):
	serializer_class = customSerializers.ProductSerializer

	def get_queryset(self):
		q = self.request.query_params.get("q")
		qs = Product.objects.filter(name__icontains=q)
		return qs
  
product_search = ProductSearchView.as_view()


class ProductsByCategoryView(ListAPIView):
	serializer_class = customSerializers.ProductSerializer

	def get_queryset(self):
		category_name = self.kwargs.get("category_name")
		return Product.objects.filter(category__name__iexact=category_name)

products_by_category = ProductsByCategoryView.as_view()


class RecentlyViewedView(ListAPIView):
	serializer_class = customSerializers.ProductSerializer
	def get_queryset(self):
		q_list = self.request.query_params.getlist("q_list[]")
		if q_list:
			qs = Product.objects.filter(uuid__in=q_list)
		else:
			qs = Product.objects.none()
		return qs
recently_viewed = RecentlyViewedView.as_view()


class ProductDetailView(RetrieveAPIView):
	queryset=Product.objects.all()
	serializer_class = customSerializers.ProductSerializer
	def get_object(self):
		uuid = self.kwargs.get('pk')
		try:
			return Product.objects.get(uuid=uuid)
		except Product.DoesNotExist:
			raise Http404
product_detail = ProductDetailView.as_view()
