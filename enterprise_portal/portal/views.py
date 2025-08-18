from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
from .models import PortalSection, SystemCard, FactoryButton, PortalSettings, PortalAnalytics
from portal.utils import translate


def is_admin(user):
    """Check if user is admin"""
    return user.is_authenticated and user.is_staff


def portal_home(request):
    """Main portal homepage"""
    settings = PortalSettings.get_settings()

    # if settings.maintenance_mode and not request.user.is_staff:
    #     return render(request, 'portal/maintenance.html', {'settings': settings})

    # Get active sections and cards
    sections = PortalSection.objects.filter(factory=None, is_active=True).prefetch_related('cards')

    # Filter cards based on user access level
    for section in sections:
        if request.user.is_authenticated:
            if request.user.is_staff:
                # Admin can see all cards
                section.filtered_cards = section.cards.filter(is_active=True)
            else:
                # Authenticated users can see public and authenticated cards
                section.filtered_cards = section.cards.filter(
                    is_active=True,
                    access_level__in=['public', 'authenticated']
                )
        else:
            # Anonymous users can only see public cards
            section.filtered_cards = section.cards.filter(
                is_active=True,
                access_level='public'
            )

    # Get quick access buttons
    if request.user.is_authenticated:
        if request.user.is_staff:
            factory_buttons = FactoryButton.objects.filter(is_active=True)
        else:
            factory_buttons = FactoryButton.objects.filter(
                is_active=True,
                access_level__in=['public', 'authenticated']
            )
    else:
        factory_buttons = FactoryButton.objects.filter(
            is_active=True,
            access_level='public'
        )

    factory_buttons = translate(factory_buttons)
    sections = translate(sections)
    for section in sections:
        section.filtered_cards = translate(section.filtered_cards)

    context = {
        'settings': settings,
        'sections': sections,
        'factory_buttons': factory_buttons,
        'is_edit_mode': request.GET.get('edit') == '1' and request.user.is_staff,
    }

    return render(request, 'portal/home.html', context)


def factory(request):
    """Main portal homepage"""
    factory_id = request.GET.get("id", 1)
    factory_data = FactoryButton.objects.get(pk=factory_id)
    settings = PortalSettings.get_settings()

    # if settings.maintenance_mode and not request.user.is_staff:
    #     return render(request, 'portal/maintenance.html', {'settings': settings})

    # Get active sections and cards
    sections = PortalSection.objects.filter(factory_id=factory_id, is_active=True).prefetch_related('cards')

    # Filter cards based on user access level
    for section in sections:
        if request.user.is_authenticated:
            if request.user.is_staff:
                # Admin can see all cards
                section.filtered_cards = section.cards.filter(is_active=True)
            else:
                # Authenticated users can see public and authenticated cards
                section.filtered_cards = section.cards.filter(
                    is_active=True,
                    access_level__in=['public', 'authenticated']
                )
        else:
            # Anonymous users can only see public cards
            section.filtered_cards = section.cards.filter(
                is_active=True,
                access_level='public'
            )

    # Get quick access buttons
    if request.user.is_authenticated:
        if request.user.is_staff:
            factory_buttons = FactoryButton.objects.filter(is_active=True)
        else:
            factory_buttons = FactoryButton.objects.filter(
                is_active=True,
                access_level__in=['public', 'authenticated']
            )
    else:
        factory_buttons = FactoryButton.objects.filter(
            is_active=True,
            access_level='public'
        )

    factory_data = translate(factory_data)
    sections = translate(sections)
    for section in sections:
        section.filtered_cards = translate(section.filtered_cards)

    context = {
        'settings': settings,
        'sections': sections,
        'factory': factory_data,
        'factory_id': factory_id,
        'is_edit_mode': request.GET.get('edit') == '1' and request.user.is_staff,
    }

    return render(request, 'portal/factory.html', context)


def portal_login_view(request):
    """Portal login view"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'portal/login.html')


def portal_logout_view(request):
    """Portal logout view"""
    logout(request)
    return redirect('home')


@user_passes_test(is_admin)
def edit_mode(request):
    """Edit mode for admin users"""
    factory_id = request.GET.get('factory')
    factory_data = None
    if factory_id:
        factory_data = FactoryButton.objects.get(pk=factory_id)
        sections = PortalSection.objects.filter(factory_id=factory_id).prefetch_related('cards')
    else:
        sections = PortalSection.objects.filter(factory=None).prefetch_related('cards')

    factory_buttons = FactoryButton.objects.all()
    settings = PortalSettings.get_settings()

    context = {
        'mode': 'editing',
        'settings': settings,
        'sections': sections,
        'factory_buttons': factory_buttons,
        'factory_id': factory_id,
        'factory_data': factory_data,
    }

    return render(request, 'portal/edit_mode.html', context)


@user_passes_test(is_admin)
@require_http_methods(["POST"])
def update_settings(request):
    """Update portal settings via AJAX (supports text + files)"""
    try:
        settings = PortalSettings.get_settings()

        # Handle text/checkbox fields from POST
        for field in ["site_title", "theme_color", "background_color",
                      "show_status_indicators", "enable_animations", "maintenance_mode"]:
            if field in request.POST:
                value = request.POST.get(field)

                # Convert checkbox values to bool
                if value in ["true", "True", "1", "on"]:
                    value = True
                elif value in ["false", "False", "0", "off", ""]:
                    value = False

                setattr(settings, field, value)

        # Handle file uploads
        if "logo" in request.FILES:
            settings.logo = request.FILES["logo"]
        if "favicon" in request.FILES:
            settings.favicon = request.FILES["favicon"]
        if "background_image" in request.FILES:
            settings.background_image = request.FILES["background_image"]

        # Update audit info
        settings.updated_by = request.user
        settings.save()

        return JsonResponse({'success': True, 'message': 'Settings updated successfully'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@user_passes_test(is_admin)
@require_http_methods(["POST"])
def create_factory(request):
    """Create new factory button"""
    try:
        data = json.loads(request.body)
        factory = FactoryButton.objects.create(
            name=data.get('name'),
            name_vi=data.get('name_vi', ''),
            name_zh_hant=data.get('name_zh_hant', ''),
            name_zh_hans=data.get('name_zh_hans', ''),
            description=data.get('description', ''),
            description_vi=data.get('description_vi', ''),
            description_zh_hant=data.get('description_zh_hant', ''),
            description_zh_hans=data.get('description_zh_hans', ''),
            url=data.get('url'),
            icon=data.get('icon', 'industry'),
            background_color=data.get('background_color', '#6366f1'),
            text_color=data.get('text_color', '#ffffff'),
            order=data.get('order', 0),
            access_level=data.get('access_level', 'public'),
            updated_by=request.user
        )

        return JsonResponse({
            'success': True,
            'message': 'Factory created successfully',
            'factory': {
                'id': factory.id,
                'name': factory.name,
                'name_vi': factory.name_vi,
                'name_zh_hant': factory.name_zh_hant,
                'name_zh_hans': factory.name_zh_hans,
                'description': factory.description,
                'description_vi': factory.description_vi,
                'description_zh_hant': factory.description_zh_hant,
                'description_zh_hans': factory.description_zh_hans,
                'url': factory.url,
                'icon': factory.icon,
                'background_color': factory.background_color,
                'text_color': factory.text_color,
                'access_level': factory.access_level,
                'order': factory.order
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@user_passes_test(is_admin)
@require_http_methods(["POST"])
def update_factory(request, factory_id):
    """Update factory button"""
    try:
        data = json.loads(request.body)
        factory = get_object_or_404(FactoryButton, id=factory_id)

        for field, value in data.items():
            if hasattr(factory, field):
                setattr(factory, field, value)

        factory.updated_by = request.user
        factory.save()

        return JsonResponse({'success': True, 'message': 'Factory updated successfully'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@user_passes_test(is_admin)
@require_http_methods(["DELETE"])
def delete_factory(request, factory_id):
    """Delete factory button"""
    try:
        factory = get_object_or_404(FactoryButton, id=factory_id)
        factory.delete()
        return JsonResponse({'success': True, 'message': 'Factory deleted successfully'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@user_passes_test(is_admin)
@require_http_methods(["POST"])
def create_section(request):
    """Create new portal section"""
    try:
        data = json.loads(request.body)
        factory_id = data.get('factory')
        factory_data = None

        if factory_id:
            try:
                factory_data = FactoryButton.objects.get(pk=factory_id)
            except FactoryButton.DoesNotExist:
                factory_data = None

        section = PortalSection.objects.create(
            name=data.get('name'),
            name_vi=data.get('name_vi', ''),
            name_zh_hant=data.get('name_zh_hant', ''),
            name_zh_hans=data.get('name_zh_hans', ''),
            factory=factory_data,
            description=data.get('description', ''),
            description_vi=data.get('description_vi', ''),
            description_zh_hant=data.get('description_zh_hant', ''),
            description_zh_hans=data.get('description_zh_hans', ''),
            icon=data.get('icon', 'folder'),
            color=data.get('color', '#6366f1'),
            order=data.get('order', 0),
            updated_by=request.user
        )

        return JsonResponse({
            'success': True,
            'message': 'Section created successfully',
            'section': {
                'id': section.id,
                'name': section.name,
                'name_vi': section.name_vi,
                'name_zh_hant': section.name_zh_hant,
                'name_zh_hans': section.name_zh_hans,
                'description': section.description,
                'description_vi': section.description_vi,
                'description_zh_hant': section.description_zh_hans,
                'description_zh_hans': section.description_zh_hans,
                'icon': section.icon,
                'color': section.color,
                'order': section.order
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@user_passes_test(is_admin)
@require_http_methods(["POST"])
def update_section(request, section_id):
    """Update portal section"""
    try:
        data = json.loads(request.body)
        section = get_object_or_404(PortalSection, id=section_id)

        for field, value in data.items():
            if field == "factory":
                try:
                    value = get_object_or_404(FactoryButton, pk=value)
                except:
                    value = None
                setattr(section, field, value)
            elif hasattr(section, field):
                setattr(section, field, value)

        section.updated_by = request.user
        section.save()

        return JsonResponse({'success': True, 'message': 'Section updated successfully'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@user_passes_test(is_admin)
@require_http_methods(["DELETE"])
def delete_section(request, section_id):
    """Delete portal section"""
    try:
        section = get_object_or_404(PortalSection, id=section_id)
        section.delete()
        return JsonResponse({'success': True, 'message': 'Section deleted successfully'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@user_passes_test(is_admin)
@require_http_methods(["POST"])
def create_card(request):
    """Create new system card"""
    try:
        data = json.loads(request.body)
        card = SystemCard.objects.create(
            section_id=data.get('section_id'),
            name=data.get('name'),
            name_vi=data.get('name_vi', ''),
            name_zh_hant=data.get('name_zh_hant', ''),
            name_zh_hans=data.get('name_zh_hans', ''),
            description=data.get('description', ''),
            description_vi=data.get('description_vi', ''),
            description_zh_hant=data.get('description_zh_hant', ''),
            description_zh_hans=data.get('description_zh_hans', ''),
            url=data.get('url'),
            icon=data.get('icon', 'desktop'),
            icon_color=data.get('icon_color', '#10b981'),
            status=data.get('status', 'online'),
            order=data.get('order', 0),
            is_external=data.get('is_external', False),
            access_level=data.get('access_level', 'public'),
            updated_by=request.user
        )

        return JsonResponse({
            'success': True,
            'message': 'Card created successfully',
            'card': {
                'id': card.id,
                'name': card.name,
                'name_vi': card.name_vi,
                'name_zh_hant': card.name_zh_hant,
                'name_zh_hans': card.name_zh_hans,
                'description': card.description,
                'description_vi': card.description_vi,
                'description_zh_hant': card.description_zh_hant,
                'description_zh_hans': card.description_zh_hans,
                'url': card.url,
                'icon': card.icon,
                'icon_color': card.icon_color,
                'status': card.status
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@user_passes_test(is_admin)
@require_http_methods(["POST"])
def update_card(request, card_id):
    """Update system card"""
    try:
        data = json.loads(request.body)
        card = get_object_or_404(SystemCard, id=card_id)

        for field, value in data.items():
            if hasattr(card, field):
                setattr(card, field, value)

        card.updated_by = request.user
        card.save()

        return JsonResponse({'success': True, 'message': 'Card updated successfully'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@user_passes_test(is_admin)
@require_http_methods(["DELETE"])
def delete_card(request, card_id):
    """Delete system card"""
    try:
        card = get_object_or_404(SystemCard, id=card_id)
        card.delete()
        return JsonResponse({'success': True, 'message': 'Card deleted successfully'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@require_http_methods(["POST"])
def track_click(request, card_id):
    """Track card clicks for analytics"""
    try:
        card = get_object_or_404(SystemCard, id=card_id)

        # Get client IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')

        # Create analytics record
        PortalAnalytics.objects.create(
            card=card,
            user=request.user if request.user.is_authenticated else None,
            ip_address=ip_address,
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )

        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
