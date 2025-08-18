from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from portal.models import PortalSection, SystemCard, FactoryButton, PortalSettings


class Command(BaseCommand):
    help = 'Create sample data for the portal'

    def handle(self, *args, **options):
        # Create or get admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'is_staff': True,
                'is_superuser': True,
                'email': 'admin@example.com'
            }
        )

        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(f'Created admin user with password: admin123')

        # Create portal settings
        settings, created = PortalSettings.objects.get_or_create(
            id=1,
            defaults={
                'site_title': '企業系統入口平台',
                'site_title_en': 'Enterprise Systems Portal',
                'theme_color': '#6366f1',
                'background_color': '#f8fafc',
                'show_status_indicators': True,
                'enable_animations': True,
                'updated_by': admin_user
            }
        )

        if created:
            self.stdout.write('Created portal settings')

        # Create Enterprise Management System section
        enterprise_section, created = PortalSection.objects.get_or_create(
            name='企業管理系統',
            defaults={
                'name_en': 'Enterprise Management System',
                'description': '企業核心業務管理平台',
                'icon': 'building',
                'color': '#8b5cf6',
                'order': 1,
                'updated_by': admin_user
            }
        )

        if created:
            # Add cards to enterprise section
            cards_data = [
                {
                    'name': 'BPM 流程管理',
                    'name_en': 'BPM Process Management',
                    'description': '業務流程管理與審批系統',
                    'url': 'https://bpm.example.com',
                    'icon': 'project-diagram',
                    'icon_color': '#8b5cf6',
                    'status': 'online'
                },
                {
                    'name': 'EIP 企業入口',
                    'name_en': 'Enterprise Information Portal',
                    'description': '企業資訊入口整合平台',
                    'url': 'https://eip.example.com',
                    'icon': 'globe',
                    'icon_color': '#06b6d4',
                    'status': 'online'
                },
                {
                    'name': 'Apollo 系統',
                    'name_en': 'Apollo System',
                    'description': '企業級應用管理平台',
                    'url': 'https://apollo.example.com',
                    'icon': 'rocket',
                    'icon_color': '#f59e0b',
                    'status': 'online'
                }
            ]

            for i, card_data in enumerate(cards_data):
                SystemCard.objects.create(
                    section=enterprise_section,
                    order=i,
                    updated_by=admin_user,
                    **card_data
                )

            self.stdout.write(f'Created Enterprise Management System section with {len(cards_data)} cards')

        # Create IT Management Platform section
        it_section, created = PortalSection.objects.get_or_create(
            name='IT 管理平台',
            defaults={
                'name_en': 'IT Management Platform',
                'description': 'IT基礎、資產與服務管理',
                'icon': 'server',
                'color': '#f97316',
                'order': 2,
                'updated_by': admin_user
            }
        )

        if created:
            # Add cards to IT section
            cards_data = [
                {
                    'name': '系統測試區',
                    'name_en': 'System Testing',
                    'description': '各系統測試與驗證分區',
                    'url': 'https://testing.example.com',
                    'icon': 'flask',
                    'icon_color': '#ef4444',
                    'status': 'maintenance'
                },
                {
                    'name': '監控平台',
                    'name_en': 'Monitoring Platform',
                    'description': '系統監控與效能監控',
                    'url': 'https://monitoring.example.com',
                    'icon': 'chart-line',
                    'icon_color': '#10b981',
                    'status': 'online'
                },
                {
                    'name': 'IT 管理工具',
                    'name_en': 'IT Management Tools',
                    'description': 'IT服務管理與配置工具',
                    'url': 'https://ittools.example.com',
                    'icon': 'tools',
                    'icon_color': '#6b7280',
                    'status': 'online'
                }
            ]

            for i, card_data in enumerate(cards_data):
                SystemCard.objects.create(
                    section=it_section,
                    order=i,
                    updated_by=admin_user,
                    **card_data
                )

            self.stdout.write(f'Created IT Management Platform section with {len(cards_data)} cards')

        # Create quick access buttons
        factory_buttons_data = [
            {
                'name': 'LT版',
                'name_en': 'LT Version',
                'description': '生產管理與優化系統',
                'url': 'https://lt.example.com',
                'icon': 'industry',
                'background_color': '#3b82f6',
                'order': 1
            },
            {
                'name': 'GD版',
                'name_en': 'GD Version',
                'description': '生產管理與優化系統',
                'url': 'https://gd.example.com',
                'icon': 'cog',
                'background_color': '#10b981',
                'order': 2
            },
            {
                'name': 'LK版',
                'name_en': 'LK Version',
                'description': '生產管理與優化系統',
                'url': 'https://lk.example.com',
                'icon': 'database',
                'background_color': '#8b5cf6',
                'order': 3
            }
        ]

        for button_data in factory_buttons_data:
            FactoryButton.objects.get_or_create(
                name=button_data['name'],
                defaults={
                    **button_data,
                    'updated_by': admin_user
                }
            )

        self.stdout.write(f'Created {len(factory_buttons_data)} quick access buttons')

        self.stdout.write(
            self.style.SUCCESS(
                'Sample data created successfully!\n'
                'Admin user: admin\n'
                'Password: admin123\n'
                'You can now run the server and visit /edit/ to manage the portal.'
            )
        )