from django.contrib import admin
from .models import Product,Variation
# import admin_thumbnails

# # Register your models here.

# @admin_thumbnails.thumbnail('image')
# class ProductGalleryInline(admin.TabularInline):
#     model = ProductGallery
#     extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','price','stock','category','modified_data','is_available')
    prepopulated_fields = {'slug' : ('product_name',)}

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product','variation_category','variation_value','created_date','is_active')
    list_editable = ('is_active',)
    list_filter = ('product','variation_category','variation_value')

admin.site.register(Product, ProductAdmin)
admin.site.register(Variation,VariationAdmin)
# admin.site.register(ProductGallery)