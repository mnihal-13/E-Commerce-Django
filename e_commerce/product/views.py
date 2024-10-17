from django.shortcuts import render,redirect
from . models import Product, Customer, Review
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm
from django.http import HttpResponseForbidden


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
    reviews = product.reviews.all()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = Customer.objects.get(user=request.user)
            review.save()
            return redirect('detail_product', pk=product.id)
    else:
        form = ReviewForm()
    # To pass the context to the template through dictionary
    context={'product':product,
             'reviews': reviews,
             'form': form}
    return render(request,'product_detail.html',context)

@login_required(login_url='account')        
def review(request,pk):
    product=Product.objects.get(pk=pk)
    reviews = product.reviews.all()
    if request.method == 'POST':
        #Initializes the review form with the POST data from the request.
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            #Which user is reviewed
            review.user = Customer.objects.get(user=request.user)
            review.save()
            return redirect('detail_product', pk=product.id)
    else:
        form = ReviewForm()
        # return render(request,'product_detail.html')
    # To pass the context to the template through dictionary
    context={'product':product,
            'reviews': reviews,
            'form': form}
    return render(request,'review.html',context)

@login_required(login_url='account')
def delete_review(request, review_id, product_id):
    #Fetches the review based on the Id and the product belongs to
    review = Review.objects.get(id=review_id, product_id=product_id)
    #Checks if the user is the current logged-in user (to prevent unauthorized deletion).
    if review.user.user == request.user:
        review.delete()
        return redirect('detail_product', pk=product_id)
    else:
        return HttpResponseForbidden("You are not allowed to delete this review.")