from django import template

register=template.Library()

@register.simple_tag(name='gettotal')
def gettotal(cart):
    # Set a 0 value of total
    total=0
    # Fetched the every items in the cart
    for item in cart.added_items.all():
        # Then multiplied the quntity and price of the product and assigned to the total variable
        total+=item.quantity*item.product.price
    return total

