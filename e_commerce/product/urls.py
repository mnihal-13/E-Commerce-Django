

from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views


urlpatterns = [
    path('', views.index,name='home'),
    path('product_list',views.list_products,name='list_products'),
    #for product details while clicked on a product
    # the '/<pk>' is to give the page number
    # whenenver clicked the product the url will be product_details/1 or 2 or ..
    path('product_details/<pk>',views.detail_product,name='detail_product')

]