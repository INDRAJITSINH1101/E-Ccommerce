from django.urls import path,include
from . import views


urlpatterns = [
    path('',views.stor , name='stor'),
    path('category/<slug:category_slug>/',views.stor,name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>',views.product_detail,name='product_detail'),
    path('search/',views.search,name='search'),
]