from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from stor.models import Product,Variation
from . models import Cart,CartItem

# Create your views here.

def cart_id(request):
  cart =  request.session.session_key
  if not cart:
    cart = request.session.create()
  return cart

def add_cart(request,product_id):
  product = Product.objects.get(id=product_id) #get the product
  product_variation = []
  if request.method == 'POST':
    for item in request.POST:
      key = item
      value = request.POST[key]
    
      try:
        variation = Variation.objects.get(
        product=product,
        variation_category__iexact=key,
        variation_value__iexact=value
          )
        product_variation.append(variation)
      except Variation.DoesNotExist:
        pass


  
  try:
    cart = Cart.objects.get(cart_id=cart_id(request)) # get the cart using the cart_id present in the session
  except Cart.DoesNotExist:
    cart = Cart.objects.create(
      cart_id = cart_id(request)
    )
    cart.save()

  try:
    cart_item = CartItem.objects.get(product=product,cart=cart)
    if len(product_variation) > 0:
      cart_item.variations.clear()
      for item in product_variation:
        cart_item.variations.add(item)
    cart_item.quantity += int(request.POST.get('quantity', 1))
        # cart_item.quentity = cart_item.quantity + 1
    cart_item.save()
  except CartItem.DoesNotExist:
    cart_item = CartItem.objects.create(
    product = product,
    quantity = int(request.POST.get('quantity', 1)),
    cart = cart,
    )

    if len(product_variation) > 0:
      cart_item.variations.clear()
      for item in product_variation:
        cart_item.variations.add(item)
    cart_item.save()
  return redirect('cart')




def remove_cart(request, product_id):
  cart = Cart.objects.get(cart_id=cart_id(request))
  product = get_object_or_404(Product, id=product_id)
  cart_item = CartItem.objects.get(product=product,cart=cart)
  if cart_item.quantity > 1 :
    cart_item.quantity -= 1
    cart_item.save()
  else:
    cart_item.delete()
  return redirect('cart')

def remove_cart_item(request,product_id):
  cart = Cart.objects.get(cart_id=cart_id(request))
  product = get_object_or_404(Product, id=product_id)
  cart_item = CartItem.objects.filter(product=product,cart=cart)
  cart_item.delete()
  return redirect('cart')


def cart(request,total=0,quantity=0,cart_items=None):
  try:
    cart = Cart.objects.get(cart_id=cart_id(request))
    cart_items = CartItem.objects.filter(cart=cart,is_active=True)
    for cart_item in cart_items:
      total += (cart_item.product.price * cart_item.quantity)
      quantity += cart_item.quantity
    tax = (2 * total)/100
    grand_total = total + tax
  except Cart.ObjectNotExixts:
    pass # just ignore

  context = {
    'total':total,
    'quantity':quantity,
    'cart_items':cart_items,
    'tax':tax,
    'grand_total':grand_total,
  }
  return render(request,'stor/cart.html',context)
