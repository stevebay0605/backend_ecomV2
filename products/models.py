from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True,)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name="Catégorie"
        verbose_name_plural="Catégories"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE , verbose_name="Catégorie")
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True,)
    description = models.TextField(blank=True)
    image=models.ImageField(upload_to='products/', blank=True , null=True, verbose_name="Image")
    price = models.DecimalField(max_digits=10, decimal_places=2 , verbose_name="Prix")
    stock = models.PositiveIntegerField(default=0 ,verbose_name="Stock")
    available = models.BooleanField(default=True)
    featured = models.BooleanField(default=False , verbose_name="En avant")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name="Produit"
        verbose_name_plural="Produits"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

