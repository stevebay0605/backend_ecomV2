from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from decimal import Decimal
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from .serializers import UserSerializer, RegisterSerializer

from products.models import Product, Category
from orders.models import Order, OrderItem
from cms.models import SiteSettings, Page, Banner
from .serializers import (
    ProductSerializer, CategorySerializer, OrderSerializer,
    SiteSettingsSerializer, PageSerializer, BannerSerializer
)

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(available=True)
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category')
        featured = self.request.query_params.get('featured')
        search = self.request.query_params.get('search')
        
        if category:
            queryset = queryset.filter(category__slug=category)
        if featured:
            queryset = queryset.filter(featured=True)
        if search:
            queryset = queryset.filter(name__icontains=search)
        
        return queryset

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    """
    Créer une commande - TOUTE la logique métier ici !
    """
    data = request.data
    items_data = data.get('items', [])
    
    # ✅ Validation 1 : Panier non vide
    if not items_data:
        return Response(
            {'error': 'Le panier est vide'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # ✅ Validation 2 : Les produits existent
    product_ids = [item['product_id'] for item in items_data]
    products = Product.objects.filter(id__in=product_ids, available=True)
    
    if len(products) != len(product_ids):
        return Response(
            {'error': 'Certains produits ne sont plus disponibles'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # ✅ Validation 3 : Stock suffisant
    products_dict = {p.id: p for p in products}
    for item in items_data:
        product = products_dict[item['product_id']]
        if product.stock < item['quantity']:
            return Response(
                {'error': f'Stock insuffisant pour {product.name}. Stock disponible: {product.stock}'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    # ✅ Calcul 1 : Total des produits
    subtotal = Decimal('0.00')
    for item in items_data:
        product = products_dict[item['product_id']]
        # ⚠️ IMPORTANT : On utilise le prix de la DB, pas celui du frontend !
        item_total = product.price * item['quantity']
        subtotal += item_total
    
    # ✅ Calcul 2 : Frais de livraison
    settings = SiteSettings.load()
    if subtotal >= settings.free_shipping_threshold:
        shipping_cost = Decimal('0.00')
    else:
        shipping_cost = settings.shipping_cost
    
    # ✅ Calcul 3 : Total final
    total = subtotal + shipping_cost
    
    # ✅ Création : Commande
    order = Order.objects.create(
        user=request.user if request.user.is_authenticated else None,
        email=data.get('email'),
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        phone=data.get('phone', ''),
        address=data.get('address'),
        postal_code=data.get('postal_code'),
        city=data.get('city'),
        total_amount=total,
        shipping_cost=shipping_cost,
        status='pending'
    )
    
    # ✅ Création : Items de commande
    for item in items_data:
        product = products_dict[item['product_id']]
        OrderItem.objects.create(
            order=order,
            product=product,
            price=product.price,  # Prix au moment de la commande
            quantity=item['quantity']
        )
        
        # ✅ Mise à jour : Décrémenter le stock
        product.stock -= item['quantity']
        product.save()
    
    # ✅ Réponse avec la commande créée
    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_site_settings(request):
    settings = SiteSettings.load()
    serializer = SiteSettingsSerializer(settings)
    return Response(serializer.data)

@api_view(['GET'])
def get_homepage_content(request):
    banners = Banner.objects.filter(is_active=True)
    featured_products = Product.objects.filter(available=True, featured=True)[:8]
    
    return Response({
        'banners': BannerSerializer(banners, many=True).data,
        'featured_products': ProductSerializer(featured_products, many=True).data
    })

class PageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Page.objects.filter(is_active=True)
    serializer_class = PageSerializer
    lookup_field = 'slug'

@api_view(['POST'])
def register(request):
    """Inscription d'un nouveau client"""
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = User.objects.create_user(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password'],
            first_name=serializer.validated_data['first_name'],
            last_name=serializer.validated_data['last_name']
        )
        return Response({
            'user': UserSerializer(user).data,
            'message': 'Compte créé avec succès'
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_user_profile(request):
    """Récupérer le profil de l'utilisateur connecté"""
    if not request.user.is_authenticated:
        return Response(
            {'error': 'Non authentifié'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['PUT'])
def update_user_profile(request):
    """Mettre à jour le profil"""
    if not request.user.is_authenticated:
        return Response(
            {'error': 'Non authentifié'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    user = request.user
    data = request.data
    
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.email = data.get('email', user.email)
    user.save()
    
    serializer = UserSerializer(user)
    return Response(serializer.data)

@api_view(['GET'])
def get_user_orders(request):
    """Historique des commandes de l'utilisateur"""
    if not request.user.is_authenticated:
        return Response(
            {'error': 'Non authentifié'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    orders = Order.objects.filter(user=request.user)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)
    