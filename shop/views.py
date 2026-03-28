from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product

def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {
        'categories': categories,
        'products': products
    }
    return render(request,'index.html', context)

def product_by_category(request, category_slug):
    categories = Category.objects.all()
    category = Category.objects.get(slug=category_slug)
    products = Product.objects.filter(category=category)
    
    context = {
        'categories': categories, 
        'products': products
    }
    return render(request, 'index.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    context = {
        'product': product
    }
    
    return render(request, 'detail.html', context)

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    context = {
        'category': category
    }
    
    return render(request, 'category.html', context)

def cart_view(request):
    return render(request, 'cart.html')