from django.shortcuts import render
from stor.models import Product

# Create your views here.

def Home(request):
  products = Product.objects.all().filter(is_available=True)

  context = {
    'products':products
  }
  
  return render(request,'home.html',context)
