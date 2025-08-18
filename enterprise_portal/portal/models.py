from django.db import models
from django.contrib.auth.models import User
from django.core.validators import URLValidator
import json


class FactoryButton(models.Model):
    """Factory buttons in the middle section"""
    name = models.CharField(max_length=50)
    name_en = models.CharField(max_length=50, blank=True, null=True)
    name_vi = models.CharField(max_length=100, blank=True)
    name_zh_hant = models.CharField(max_length=100, blank=True)
    name_zh_hans = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    description_vi = models.TextField(blank=True)
    description_zh_hant = models.TextField(blank=True)
    description_zh_hans = models.TextField(blank=True)
    url = models.URLField(validators=[URLValidator()])
    icon = models.CharField(max_length=50, default='link')
    background_color = models.CharField(max_length=7, default='#3b82f6')
    text_color = models.CharField(max_length=7, default='#ffffff')
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    access_level = models.CharField(
        max_length=20,
        choices=[
            ('public', 'Public'),
            ('authenticated', 'Authenticated'),
            ('admin', 'Admin'),
        ],
        default='public'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class PortalSection(models.Model):
    """Main sections of the portal"""
    factory = models.ForeignKey(FactoryButton, on_delete=models.DO_NOTHING, related_name='section_factory',
                                null=True, blank=False, default=None)
    name = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100, blank=True, null=True)
    name_vi = models.CharField(max_length=100, blank=True)
    name_zh_hant = models.CharField(max_length=100, blank=True)
    name_zh_hans = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    description_vi = models.TextField(blank=True)
    description_zh_hant = models.TextField(blank=True)
    description_zh_hans = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='folder')  # CSS icon class
    color = models.CharField(max_length=7, default='#6366f1')  # Hex color
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class SystemCard(models.Model):
    """Individual system cards within sections"""
    section = models.ForeignKey(PortalSection, on_delete=models.CASCADE, related_name='cards')
    name = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100, blank=True, null=True)
    name_vi = models.CharField(max_length=100, blank=True)
    name_zh_hant = models.CharField(max_length=100, blank=True)
    name_zh_hans = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    description_vi = models.TextField(blank=True)
    description_zh_hant = models.TextField(blank=True)
    description_zh_hans = models.TextField(blank=True)
    url = models.URLField(validators=[URLValidator()])
    icon = models.CharField(max_length=50, default='desktop')  # CSS icon class
    icon_color = models.CharField(max_length=7, default='#10b981')  # Hex color
    status = models.CharField(
        max_length=20,
        choices=[
            ('online', 'Online'),
            ('offline', 'Offline'),
            ('maintenance', 'Maintenance'),
        ],
        default='online'
    )
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_external = models.BooleanField(default=False)  # Opens in new tab
    access_level = models.CharField(
        max_length=20,
        choices=[
            ('public', 'Public'),
            ('authenticated', 'Authenticated'),
            ('admin', 'Admin'),
        ],
        default='public'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.section.name} - {self.name}"


class PortalSettings(models.Model):
    """Global portal settings"""
    site_title = models.CharField(max_length=100, default='Enterprise Systems Portal')
    site_title_en = models.CharField(max_length=100, default='Enterprise Systems Portal')
    site_logo = models.ImageField(upload_to='portal/logos/', blank=True, null=True)
    logo = models.ImageField(upload_to="logo/", blank=True, null=True)
    favicon = models.ImageField(upload_to="favicon/", blank=True, null=True)
    background_image = models.ImageField(upload_to="background/", blank=True, null=True)
    theme_color = models.CharField(max_length=7, default='#6366f1')
    background_color = models.CharField(max_length=7, default='#f8fafc')
    show_status_indicators = models.BooleanField(default=True)
    enable_animations = models.BooleanField(default=True)
    maintenance_mode = models.BooleanField(default=False)
    maintenance_message = models.TextField(blank=True)
    custom_css = models.TextField(blank=True, help_text="Custom CSS styles")
    custom_js = models.TextField(blank=True, help_text="Custom JavaScript")
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Portal Settings"
        verbose_name_plural = "Portal Settings"

    def __str__(self):
        return "Portal Settings"

    @classmethod
    def get_settings(cls):
        """Get or create portal settings"""
        settings, created = cls.objects.get_or_create(id=1)
        return settings


class PortalAnalytics(models.Model):
    """Track portal usage analytics"""
    card = models.ForeignKey(SystemCard, on_delete=models.CASCADE, related_name='analytics')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    clicked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-clicked_at']

    def __str__(self):
        return f"{self.card.name} - {self.clicked_at}"