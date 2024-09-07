from django import template

register=template.Library()

# For multiplying the product price when added same prodcut multiple time
# It multiply the price of product with the number of qunatity 
@register.simple_tag(name='multiply')
def multiply(a,b):
    return a*b
