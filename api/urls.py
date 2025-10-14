from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

router = DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('categories', views.CategoryViewSet)
router.register('pages', views.PageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('orders/create/', views.create_order, name='create-order'),
    path('settings/', views.get_site_settings, name='site-settings'),
    path('homepage/', views.get_homepage_content, name='homepage-content'),
    # ===== AUTHENTIFICATION =====
    # Login (obtenir le token)
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Refresh token
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Register
    path('auth/register/', views.register, name='register'),
    
    # Profile
    path('auth/profile/', views.get_user_profile, name='user-profile'),
    path('auth/profile/update/', views.update_user_profile, name='update-profile'),
    
    # Commandes de l'utilisateur
    path('auth/orders/', views.get_user_orders, name='user-orders'),
]