from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from landing.models import (
    SiteSettings, Disease, TourFeature, 
    TreatmentCategory, TreatmentItem, Lead, GalleryPhoto
)


class NaftalanProjectTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_superuser('testadmin', 'admin@masuf.uz', 'pass123')
        self.manager_user = User.objects.create_user('testmanager', 'manager@masuf.uz', 'pass123')
        
        self.settings = SiteSettings.objects.create(
            site_title_uz="Test Naftalan UZ",
            site_title_ru="Test Naftalan RU",
            hero_title_uz="Test Hero Title UZ",
            hero_title_ru="Test Hero Title RU",
            tour_price="1350$",
            flight_dates_uz="08.10.2026 (7 kecha)",
            flight_dates_ru="08.10.2026 (7 ночей)",
            phone_number="+998994111151"
        )
        self.disease = Disease.objects.create(
            title_uz="Bo'g'im kasalliklari",
            title_ru="Заболевания суставов",
            icon="fas fa-bone",
            order=1
        )
        self.feature = TourFeature.objects.create(
            title_uz="5* Mehmonxona",
            title_ru="5* Отель",
            icon="fas fa-hotel",
            order=1
        )
        self.category = TreatmentCategory.objects.create(
            title_uz="Shifokor qabuli",
            title_ru="Приемы врачей",
            icon="fas fa-user-md",
            order=1
        )
        self.item = TreatmentItem.objects.create(
            category=self.category,
            name_uz="Dastlabki ko'rik",
            name_ru="Первичный осмотр",
            order=1
        )
        self.media_photo = GalleryPhoto.objects.create(
            title_uz="Test Rasm UZ",
            title_ru="Test Фото RU",
            media_type="video_url",
            video_url="https://youtube.com/watch?v=12345",
            category="hotel",
            order=1
        )

    def test_landing_page_default_uz(self):
        response = self.client.get(reverse('landing_page'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Hero Title UZ")
        self.assertContains(response, "1350$")
        self.assertContains(response, "5* Mehmonxona")
        self.assertContains(response, "Shifokor qabuli")
        self.assertContains(response, "Test Rasm UZ")

    def test_landing_page_russian_switch(self):
        response = self.client.get(reverse('landing_page') + '?lang=ru')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Hero Title RU")
        self.assertContains(response, "Заболевания суставов")
        self.assertContains(response, "5* Отель")
        self.assertContains(response, "Приемы врачей")
        self.assertContains(response, "Test Фото RU")

    def test_lead_submission_ajax(self):
        data = {
            'name': 'Ali Valiyev',
            'phone': '+998901234567',
            'message': 'Naftalan haqida ma\'lumot bering',
            'source': 'landing_form'
        }
        response = self.client.post(
            reverse('submit_lead'), 
            data, 
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Lead.objects.filter(name='Ali Valiyev').exists())

    def test_dashboard_login_required(self):
        response = self.client.get(reverse('dashboard_home'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/dashboard/login/', response.url)

    def test_dashboard_authenticated(self):
        self.client.login(username='testmanager', password='pass123')
        response = self.client.get(reverse('dashboard_home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Boshqaruv Paneli")

    def test_dashboard_settings_update(self):
        self.client.login(username='testadmin', password='pass123')
        data = {
            'site_title_uz': 'Yangilangan Naftalan UZ',
            'site_title_ru': 'Yangilangan Naftalan RU',
            'hero_badge_uz': 'Yangi Badge UZ',
            'hero_badge_ru': 'Yangi Badge RU',
            'hero_title_uz': 'Yangi Katta Sarlavha UZ',
            'hero_title_ru': 'Yangi Katta Sarlavha RU',
            'hero_subtitle_uz': 'Yangi tavsif UZ',
            'hero_subtitle_ru': 'Yangi tavsif RU',
            'about_text_uz': 'Yangi matn UZ',
            'about_text_ru': 'Yangi matn RU',
            'hero_media_type': 'image',
            'flight_dates_uz': '08.10.2026 (7 kecha 8 kun)',
            'flight_dates_ru': '08.10.2026 (7 ночей 8 дней)',
            'tour_price': '1400$',
            'hotel_name_uz': '5* Gashalti UZ',
            'hotel_name_ru': '5* Gashalti RU',
            'phone_number': '+998919686886',
            'phone_number_2': '+998974111151',
            'operator_name': 'Abduqodir',
            'telegram_url': 'https://t.me/khalilov1999',
            'instagram_url': 'https://www.instagram.com/masuftravel?stkn=MWlpN2J2NXJ0d2dpaA==',
            'location_url': 'https://yandex.ru/maps/-/CTxuVNMr',
            'whatsapp_url': '',
        }
        response = self.client.post(reverse('dashboard_settings'), data)

        self.assertEqual(response.status_code, 302)
        self.settings.refresh_from_db()
        self.assertEqual(self.settings.tour_price, '1400$')
        self.assertEqual(self.settings.site_title_uz, 'Yangilangan Naftalan UZ')
        self.assertEqual(self.settings.site_title_ru, 'Yangilangan Naftalan RU')

    def test_dashboard_gallery_crud(self):
        self.client.login(username='testadmin', password='pass123')
        
        # Gallery list
        response = self.client.get(reverse('dashboard_gallery'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Rasm UZ")

        # Gallery edit
        edit_data = {
            'title_uz': 'Tahrirlangan Rasm UZ',
            'title_ru': 'Отредактированное фото RU',
            'media_type': 'video_url',
            'video_url': 'https://youtube.com/watch?v=99999',
            'category': 'treatment',
            'order': 5,
            'is_active': True
        }
        edit_resp = self.client.post(reverse('dashboard_gallery_edit', kwargs={'pk': self.media_photo.id}), edit_data)
        self.assertEqual(edit_resp.status_code, 302)
        self.media_photo.refresh_from_db()
        self.assertEqual(self.media_photo.title_uz, 'Tahrirlangan Rasm UZ')
        self.assertEqual(self.media_photo.order, 5)

        # Gallery delete
        del_resp = self.client.post(reverse('dashboard_gallery_delete', kwargs={'pk': self.media_photo.id}))
        self.assertEqual(del_resp.status_code, 302)
        self.assertFalse(GalleryPhoto.objects.filter(id=self.media_photo.id).exists())


