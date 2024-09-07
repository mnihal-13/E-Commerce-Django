from django.shortcuts import render
from . models import Product
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    # To show the fist 4 featured products in the home page with base of priority by indexing 
    featured_products=Product.objects.order_by('priority')[:3]
    latest_products=Product.objects.order_by('-id')[:3]
    context={
        'featured_products':featured_products,
        'latest_products':latest_products
    }
    return render(request,'index.html',context)

def list_products(request):
    """
    returns prouduct list page
    """
    page=1
    # To get the page user requested
    if request.GET:
        page=request.GET.get('page',1)
    #To show the product fetched from the backend
    # 'order_by'--To sort the products by the given argument
    product_list=Product.objects.order_by('priority')
    # To show the 4 product from the server while on the product page from the product list
    product_paginator=Paginator(product_list,8)
    # To show the page requseted by the user
    product_list=product_paginator.get_page(page)
    # To pass the data with dictionary
    context={'products':product_list}
    return render(request,'products.html',context)

def detail_product(request,pk):
    # To fetch the product clicked by the id
    product=Product.objects.get(pk=pk)
    # To pass the context to the template through dictionary
    context={'product':product}
    return render(request,'product_detail.html',context)