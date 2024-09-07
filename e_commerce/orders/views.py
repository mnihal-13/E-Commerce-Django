from django.shortcuts import render,redirect
from .models import Order,OrderedItem
from django.contrib import messages
from product.models import Product
from django.contrib.auth.decorators import login_required

# Create your views here.
def show_cart(request):
    user=request.user
    customer=user.customer_profile
    print("user",user)
    print("customer",customer)
    cart_obj,created=Order.objects.get_or_create(
            owner=customer,
            order_status=Order.CART_STAGE
        )
    context={'cart':cart_obj}

    return render(request,'cart.html',context)

# For removing the items from the cart
def remove_item_from_cart(request,pk):
    # Fetched the ordered items with the primary key
    item=OrderedItem.objects.get(pk=pk)
    # If the item is exist delete the items and redirect to cart
    if item:
        item.delete()
    return redirect('cart')


def checkout_cart(request):
    
    if request.POST:
        try:
            user=request.user
            customer=user.customer_profile
            total=float(request.POST.get('total'))
            print(total)
            order_obj=Order.objects.get(
                owner=customer,
                order_status=Order.CART_STAGE
            )
            # If oder_obj is True
            if order_obj:
                # Changed the status iof the order_obj to confirmed
                order_obj.order_status=Order.ORDER_CONFIRMED
                order_obj.total_price=total
                order_obj.save()
                print("price",order_obj.total_price)
                status_message="Your order is processed. Your item will be delivered with in 2 days"
                messages.success(request,status_message)
            else:
                status_message="unable to processed. No items in cart"
                messages.error(request,status_message)
        except Exception as e:
                status_message="unable to processed. No items in cart"
                messages.error(request,status_message)
    return redirect('cart')


@login_required(login_url='account')        
def show_orders(request):
    user=request.user
    customer=user.customer_profile
    all_orders=Order.objects.filter(owner=customer).exclude(order_status=Order.CART_STAGE)
    context={'orders':all_orders}
    return render(request,'orders.html',context)



@login_required(login_url='account')
def add_to_cart(request):
    if request.POST:
        # To fetch which user is loged in
        user=request.user
        print(user)
        # To fetch the reverse relationship of the users customer profile
        customer=user.customer_profile
        print(customer)
        # To get the number of quntity of the product in the cart
        quantity=int(request.POST.get('quantity'))
        # To fetch the product id
        product_id=request.POST.get('product_id')
        # While logging a new user there is no products or order in the cart for that get_or_create method is given
        # It returns a tuple with two value. One is ordered product and other is a boolean value
        cart_obj,created=Order.objects.get_or_create(
            owner=customer,
            order_status=Order.CART_STAGE
        )
        #We geted the product model with the product id
        product=Product.objects.get(pk=product_id)
        #'get_or_create' is used, if the prodcut is in cart get the item or else no product create the product to the cart
        ordered_item,created=OrderedItem.objects.get_or_create(
            #Given the product object to the variable
            product=product,
            owner=cart_obj
        )
        #To check if the procut is created or new item
        # add the items quntity and save
        if created:
            ordered_item.quantity=quantity
            ordered_item.save()
        else:
            #if the item is already in the cart and added same prodcut to the cart
            # add the current prodcuts quntity number and save
            ordered_item.quantity=ordered_item.quantity+quantity
            ordered_item.save()
    return redirect('cart')