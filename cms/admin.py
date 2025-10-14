from django.contrib import admin
from .models import SiteSettings, Page, Banner

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Informations Générales', {
            'fields': ['site_name', 'tagline', 'logo']
        }),
        ('Contact', {
            'fields': ['contact_email', 'contact_phone']
        }),
        ('Réseaux Sociaux', {
            'fields': ['facebook_url', 'instagram_url', 'twitter_url']
        }),
        ('Livraison', {
            'fields': ['free_shipping_threshold', 'shipping_cost']
        }),
    ]
    
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'is_active', 'updated']
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ['is_active']
    search_fields = ['title', 'content']

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    list_filter = ['is_active']