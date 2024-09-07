from django.contrib import admin
from orders.models import Order,OrderedItem

# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    # To filter in admin with respect to order status and owner in the db
    list_filter = [
         "owner",
         "order_status",
    ]
    # For search field with the given value
    search_fields = (
        "owner",
        "id",
    )
  
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderedItem)
