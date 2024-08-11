import uuid
from django.db import models


class Category(models.Model):
  name = models.CharField(max_length=30)

  class Meta:
    verbose_name_plural = "Categories"
  
  def __str__(self):
    return self.name
    

class Brand(models.Model):
  category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
  name = models.CharField(max_length=30)
  
  def __str__(self):
    return self.name
  
class Product(models.Model):
  AVAILABILITY_STATUS_CHOICES = (
    (1,"Available"),
    (0, "Unavailable")
  )
  UTILIZATION_STATUS_CHOICES = (
    (0,"Brand New"),
    (1, "UK Used")
  )
  uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
  category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
  brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)
  name = models.CharField(max_length=30)
  description = models.TextField()
  price = models.DecimalField(max_digits=15, decimal_places=2)
  image = models.ImageField(upload_to="products/%Y/%m")
  stock = models.IntegerField()
  availability_status = models.IntegerField(choices=AVAILABILITY_STATUS_CHOICES)
  utilization_status = models.IntegerField(choices=UTILIZATION_STATUS_CHOICES)
  created_at = models.DateTimeField(auto_now_add=True)
  
  
  def __str__(self):
    return self.name