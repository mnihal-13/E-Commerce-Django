from django import template

register=template.Library()

@register.simple_tag(name='getstatus')
# This will show the order status to the user by changing the value in the db
def getstatus(status):
    # To avoid the zeroth staus
    status=status-1
    status_array=['confirmed','processed','delivered','rejected']
    return  status_array[status]

