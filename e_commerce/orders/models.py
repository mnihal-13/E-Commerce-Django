from django.db import models
from customers.models import Customer
from product.models import Product

#Data model for orders
class Order(models.Model):
    LIVE=1
    DELETE=0
    DELETE_CHOICES=((LIVE,'Live'),(DELETE,'Delete'))
    CART_STAGE=0
    ##Order Statuses
    ORDER_CONFIRMED=1
    ORDER_PROCESSED=2
    ORDER_DELIVERED=3
    ORDER_REJECTED=4
    ##All set to a variable and set into a tuple
    STATUS_CHOICE=((ORDER_PROCESSED,"ORDER_PROCESSED"),
                   (ORDER_DELIVERED,"ORDER_DELIVERED"),
                   (ORDER_REJECTED,"ORDER_REJECTED"),
                   (ORDER_CONFIRMED,"ORDER_CONFIRMED")
                   )
    #Set a variable of the order status and given the choice to the STATUS_ORDER
    #Set default value to CART_STAGE
    order_status=models.IntegerField(choices=STATUS_CHOICE,default=CART_STAGE)
    total_price=models.FloatField(default=0)
    ##OneToMany relationship with the customer
    ##One user have multiple products or order , for that here OneToMany relation
    ##Given the customer acc as a owner
    owner=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True, related_name='orders')
    delete_status=models.IntegerField(choices=DELETE_CHOICES,default=LIVE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return "order-{}-{}".format(self.id,self.owner.name)

#model for ordered item
class OrderedItem(models.Model):
    ##To show the products items added to cart
    ##Even the product deleted, the items want show on the user ordered list, so set to SET_NULL
    product=models.ForeignKey(Product,related_name='added_carts',on_delete=models.SET_NULL,null=True)
    quantity=models.IntegerField(default=1)
    owner=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='added_items')
    