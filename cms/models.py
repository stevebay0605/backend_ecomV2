from django.db import models

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, default='SteveShop', verbose_name="Nom du site")
    tagline = models.CharField(max_length=200, blank=True, verbose_name="Slogan")
    logo = models.ImageField(upload_to='site/', blank=True, null=True, verbose_name="Logo")
    
    # Contact
    contact_email = models.EmailField(verbose_name="Email de contact")
    contact_phone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    
    # Réseaux sociaux
    facebook_url = models.URLField(blank=True, verbose_name="Facebook")
    instagram_url = models.URLField(blank=True, verbose_name="Instagram")
    twitter_url = models.URLField(blank=True, verbose_name="Twitter")
    
    # Configuration
    free_shipping_threshold = models.DecimalField(max_digits=10, decimal_places=2, default=50, verbose_name="Livraison gratuite à partir de")
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=5, verbose_name="Frais de livraison")
    
    class Meta:
        verbose_name = 'Configuration du Site'
        verbose_name_plural = 'Configuration du Site'
    
    def __str__(self):
        return self.site_name
    
    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class Page(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titre")
    slug = models.SlugField(unique=True)
    content = models.TextField(verbose_name="Contenu")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Page"
        verbose_name_plural = "Pages"
        ordering = ['title']
    
    def __str__(self):
        return self.title


class Banner(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titre")
    subtitle = models.CharField(max_length=300, blank=True, verbose_name="Sous-titre")
    image = models.ImageField(upload_to='banners/', verbose_name="Image")
    button_text = models.CharField(max_length=100, blank=True, verbose_name="Texte du bouton")
    button_link = models.CharField(max_length=200, blank=True, verbose_name="Lien du bouton")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    order = models.IntegerField(default=0, verbose_name="Ordre")
    
    class Meta:
        verbose_name = "Bannière"
        verbose_name_plural = "Bannières"
        ordering = ['order']
    
    def __str__(self):
        return self.title