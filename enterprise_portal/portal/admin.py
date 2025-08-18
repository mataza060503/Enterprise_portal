from django.contrib import admin
from django.utils.html import format_html
from .models import PortalSection, SystemCard, FactoryButton, PortalSettings, PortalAnalytics


@admin.register(PortalSettings)
class PortalSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_title', 'theme_color', 'maintenance_mode', 'updated_at', 'updated_by')
    readonly_fields = ('updated_at', 'updated_by')
    fieldsets = (
        ('Basic Settings', {
            'fields': ('site_title', 'site_title_en', 'site_logo')
        }),
        ('Appearance', {
            'fields': ('theme_color', 'background_color', 'show_status_indicators', 'enable_animations')
        }),
        ('Maintenance', {
            'fields': ('maintenance_mode', 'maintenance_message')
        }),
        ('Custom Code', {
            'fields': ('custom_css', 'custom_js'),
            'classes': ('collapse',)
        }),
        ('Meta', {
            'fields': ('updated_at', 'updated_by'),
            'classes': ('collapse',)
        })
    )

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class SystemCardInline(admin.TabularInline):
    model = SystemCard
    extra = 0
    fields = ('name', 'url', 'icon', 'status', 'access_level', 'order', 'is_active')
    ordering = ('order', 'name')


@admin.register(PortalSection)
class PortalSectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_en', 'color_display', 'card_count', 'order', 'is_active', 'updated_at')
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('name', 'name_en', 'description')
    ordering = ('order', 'name')
    inlines = [SystemCardInline]
    readonly_fields = ('created_at', 'updated_at', 'updated_by')

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'name_en', 'description')
        }),
        ('Appearance', {
            'fields': ('icon', 'color', 'order')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Meta', {
            'fields': ('created_at', 'updated_at', 'updated_by'),
            'classes': ('collapse',)
        })
    )

    def color_display(self, obj):
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {}; border: 1px solid #ccc; border-radius: 3px;"></div>',
            obj.color
        )

    color_display.short_description = 'Color'

    def card_count(self, obj):
        return obj.cards.count()

    card_count.short_description = 'Cards'

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(SystemCard)
class SystemCardAdmin(admin.ModelAdmin):
    list_display = ('name', 'section', 'url_display', 'status_display', 'access_level', 'order', 'is_active')
    list_filter = ('section', 'status', 'access_level', 'is_active', 'is_external', 'created_at')
    search_fields = ('name', 'name_en', 'description', 'url')
    ordering = ('section__order', 'order', 'name')
    readonly_fields = ('created_at', 'updated_at', 'updated_by', 'click_count')

    fieldsets = (
        ('Basic Information', {
            'fields': ('section', 'name', 'name_en', 'description', 'url')
        }),
        ('Appearance', {
            'fields': ('icon', 'icon_color')
        }),
        ('Settings', {
            'fields': ('status', 'access_level', 'is_external', 'order')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Analytics', {
            'fields': ('click_count',),
            'classes': ('collapse',)
        }),
        ('Meta', {
            'fields': ('created_at', 'updated_at', 'updated_by'),
            'classes': ('collapse',)
        })
    )

    def url_display(self, obj):
        return format_html('<a href="{}" target="_blank">{}</a>', obj.url,
                           obj.url[:50] + '...' if len(obj.url) > 50 else obj.url)

    url_display.short_description = 'URL'

    def status_display(self, obj):
        colors = {
            'online': '#10b981',
            'offline': '#ef4444',
            'maintenance': '#f59e0b'
        }
        return format_html(
            '<span style="color: {}; font-weight: bold;">● {}</span>',
            colors.get(obj.status, '#6b7280'),
            obj.get_status_display()
        )

    status_display.short_description = 'Status'

    def click_count(self, obj):
        return obj.analytics.count()

    click_count.short_description = 'Total Clicks'

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(FactoryButton)
class FactoryButtonAdmin(admin.ModelAdmin):
    list_display = ('name', 'url_display', 'color_display', 'access_level', 'order', 'is_active')
    list_filter = ('access_level', 'is_active', 'created_at')
    search_fields = ('name', 'name_en', 'description', 'url')
    ordering = ('order', 'name')
    readonly_fields = ('created_at', 'updated_at', 'updated_by')

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'name_en', 'description', 'url')
        }),
        ('Appearance', {
            'fields': ('icon', 'background_color', 'text_color', 'order')
        }),
        ('Settings', {
            'fields': ('access_level', 'is_active')
        }),
        ('Meta', {
            'fields': ('created_at', 'updated_at', 'updated_by'),
            'classes': ('collapse',)
        })
    )

    def url_display(self, obj):
        return format_html('<a href="{}" target="_blank">{}</a>', obj.url,
                           obj.url[:50] + '...' if len(obj.url) > 50 else obj.url)

    url_display.short_description = 'URL'

    def color_display(self, obj):
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {}; border: 1px solid #ccc; border-radius: 3px;"></div>',
            obj.background_color
        )

    color_display.short_description = 'Color'

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(PortalAnalytics)
class PortalAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('card', 'user', 'ip_address', 'clicked_at')
    list_filter = ('clicked_at', 'card__section', 'card')
    search_fields = ('card__name', 'user__username', 'ip_address')
    readonly_fields = ('card', 'user', 'ip_address', 'user_agent', 'clicked_at')
    ordering = ('-clicked_at',)

    def has_add_permission(self, request):
        return False  # Prevent manual creation

    def has_change_permission(self, request, obj=None):
        return False  # Prevent editing