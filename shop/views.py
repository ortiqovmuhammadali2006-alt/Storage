from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Product, Order, OrderProduct, ShippingAddress
from django.contrib import messages


def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {"categories": categories, "products": products}
    return render(request, "index.html", context)


def product_by_category(request, category_slug):
    categories = Category.objects.all()
    category = Category.objects.get(slug=category_slug)
    products = Product.objects.filter(category=category)

    context = {"categories": categories, "products": products}
    return render(request, "index.html", context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    context = {"product": product}

    return render(request, "detail.html", context)


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    context = {"category": category}

    return render(request, "category.html", context)


@login_required(login_url="login")
def cart_view(request):
    return render(request, "cart.html")


@login_required(login_url="login")
def add_to_cart(request, product_slug):

    if request.method != "POST":
        return redirect("home")

    product = get_object_or_404(Product, slug=product_slug, is_aviable=True)

    order, created = Order.objects.get_or_create(
        user=request.user, is_ordered=False, defaults={"total_price": 0}
    )

    order_item, item_created = OrderProduct.objects.get_or_create(
        order=order, product=product, defaults={"quantity": 1, "price": product.price}
    )
    
    
    if not item_created:
        order_item.quantity += 1
        order_item.save()
    
    
    order.total_price = sum(item.get_total_price() for item in order.items.all())
    order.save()
    
    messages.success(request, "Mahsulot savatga qo'shildi")
    
    
    

    return redirect("home")
