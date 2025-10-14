from django.db import models
from django.contrib.auth.models import User
from products.models import Product
import uuid


class Order(models.Model):
    STATUT_CHOICES = [
        ('PENDING', 'en attente'),
        ('PAID', 'payée'),
        ('PROCESSING', 'en cours de traitement'),
        ('SHIPPED', 'expédiée'),
        ('DELIVERED', 'livrée'),
        ('CANCELLED', 'annulée'),
    ]

    order_number=models.CharField(max_length=32, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')


#information du client
    email = models.EmailField()
    first_name = models.CharField(max_length=50, verbose_name='prénom')
    last_name = models.CharField(max_length=50, verbose_name='nom ')
    phone = models.CharField(max_length=20, verbose_name='téléphone', blank=True)

#information de livraison
    address = models.CharField(max_length=255, verbose_name='adresse')
    city = models.CharField(max_length=100, verbose_name='ville')
    postal_code = models.CharField(max_length=20, verbose_name='code postal')

#informations de paiement

    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='montant total')
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='frais de livraison', default=0)

#statut de la commande
    status = models.CharField(max_length=20, choices=STATUT_CHOICES, default='PENDING')
    created= models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
        verbose_name = 'commande'
        verbose_name_plural = 'commandes'

    def __str__(self):
        return f'Commande {self.order_number}'

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f'ORD-{uuid.uuid4().hex[:8].upper()}'
        super().save(*args, **kwargs)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1 , verbose_name='quantité')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='prix')

    class Meta:
        verbose_name = 'article de commande'
        verbose_name_plural = 'articles de commande'

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'
    
    def get_cost(self):
        return self.quantity * (self.price or 0)
