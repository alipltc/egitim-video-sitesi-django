from django.contrib import admin

# Register your models here.

from order.models import ShopCart, Order, OrderVideo


class ShopCartAdmin(admin.ModelAdmin):
    list_display = ['user', 'video', 'price', 'quantity', 'amount']
    list_filter = ['user']

class OrderVideoline(admin.TabularInline):
    model = OrderVideo
    readonly_fields = ('user','video','price','quantity','amount')
    can_delete = False
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone', 'city', 'total', 'status']
    list_filter = ['status']
    readonly_fields = ('user','address','city','country','phone','first_name','last_name','total')
    inlines = [OrderVideoline]

class OrderVideoAdmin(admin.ModelAdmin):
    list_display = ['user', 'video', 'price', 'quantity', 'amount', 'status']
    list_filter = ['user','status']

admin.site.register(ShopCart,ShopCartAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderVideo,OrderVideoAdmin)