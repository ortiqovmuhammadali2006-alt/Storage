from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from user.models import CustomUser


class Sticker(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20, default="red")

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nomi")
    slug = models.SlugField(unique=True)

    stickers = models.ManyToManyField(Sticker, blank=True)

    class Meta:
        verbose_name = "Kategoriya "
        verbose_name_plural = "Kategoriyalar"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Nomi")
    description = models.TextField(blank=True, verbose_name="Izohi")
    slug = models.SlugField(unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Narxi")
    quantity = models.IntegerField(default=0)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="Reytingi"
    )
    is_available = models.BooleanField(default=True)
    brand = models.CharField(max_length=100, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )

    class Meta:
        verbose_name = "Mahsulot "
        verbose_name_plural = "Mahsulotlar "
        ordering = ["name"]

    def __str__(self):
        return self.name
    
    def get_image(self):
        product_images = self.images.all()
        if product_images:
            return product_images[0].image.url
        else:
            return '___'


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Mahsulot",
        related_name="images",
    )
    image = models.ImageField(upload_to="products/", verbose_name="Rasmi")

    class Meta:
        verbose_name = "Mahsulot rasmi "
        verbose_name_plural = "Mahsulot rasmlari"
        ordering = ["product"]

    def __str__(self):
        return f"{self.product.name}"


class Comment(models.Model):
    text = models.TextField(max_length=255, verbose_name="Izohi")
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="Reytingi"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Foydalanuvchi",
    )
    time = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqti")

    class Meta:
        verbose_name = "Izoh "
        verbose_name_plural = "Izohlar "
        ordering = ["text"]

    def __str__(self):
        return f"{self.product.name}"


class Order(models.Model):
    STATUS_CHOICES = (
        ("pending", "Kutilmoqda"),
        ("shipped", "Yuborildi"),
        ("delivered", "Yetkazildi"),
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    user = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pk} : {self.user.first_name} {self.user.last_name}"


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_total_price(self):
        return self.quantity * self.price

    def __str__(self):
        return self.product.name


class ShippingAddress(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True
    )
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="shipping_addresses"
    )
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
