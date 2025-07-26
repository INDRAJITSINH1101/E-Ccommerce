from django.db import models
from stor.models import Product,Variation

# Create your models here.
class Cart(models.Model):
  cart_id = models.CharField(max_length=250,blank=True)
  date_added = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return str(self.cart_id)
  
class CartItem(models.Model):
  product = models.ForeignKey(Product,on_delete=models.CASCADE)
  variations = models.ManyToManyField(Variation, blank=True)
  cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
  quantity = models.IntegerField()
  is_active = models.BooleanField(default=True)

  def sub_total(self):
    return self.product.price * self.quantity

  def __str__(self):
    variations = ", ".join([f"{v.variation_category}: {v.variation_value}" for v in self.variations.all()])
    return f"{self.product.product_name} x{self.quantity} [{variations}]"


