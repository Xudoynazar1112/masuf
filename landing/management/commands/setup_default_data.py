import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from landing.models import (
    SiteSettings, Disease, TourFeature, 
    TreatmentCategory, TreatmentItem, Lead, GalleryPhoto
)
from PIL import Image, ImageDraw, ImageFont
import io


class Command(BaseCommand):
    help = "Boshlang'ich ma'lumotlar, admin va menejer foydalanuvchilarini yaratish"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Boshlang'ich ma'lumotlarni yaratish boshlandi..."))

        # 1. Admin va Menejer foydalanuvchilarini yaratish
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@masuf.uz', 'admin123')
            self.stdout.write(self.style.SUCCESS("Superuser 'admin' yaratildi (parol: admin123)"))
        else:
            self.stdout.write(self.style.WARNING("Superuser 'admin' allaqachon mavjud."))

        if not User.objects.filter(username='manager').exists():
            manager = User.objects.create_user('manager', 'manager@masuf.uz', 'manager123')
            manager.is_staff = True
            manager.save()
            self.stdout.write(self.style.SUCCESS("Menejer 'manager' yaratildi (parol: manager123)"))
        else:
            self.stdout.write(self.style.WARNING("Menejer 'manager' allaqachon mavjud."))

        # 2. Default rasmlar yaratish (agar kerak bo'lsa)
        def generate_sample_image(text, width=1200, height=800, bg_color=(20, 80, 120)):
            img = Image.new('RGB', (width, height), color=bg_color)
            draw = ImageDraw.Draw(img)
            # Chiroyli gradient/fon effekti
            for y in range(height):
                r = int(bg_color[0] + (y / height) * 30)
                g = int(bg_color[1] + (y / height) * 40)
                b = int(bg_color[2] + (y / height) * 20)
                draw.line([(0, y), (width, y)], fill=(min(r, 255), min(g, 255), min(b, 255)))
            
            # Matn chizish
            draw.text((width // 8, height // 2 - 20), text, fill=(255, 255, 255))
            buf = io.BytesIO()
            img.save(buf, format='JPEG', quality=90)
            return ContentFile(buf.getvalue())

        # 3. SiteSettings sozlamalari
        settings = SiteSettings.get_settings()
        settings.site_title_uz = "Masuf Travel - Naftalan Davolanish & Sayohat Dasturi"
        settings.site_title_ru = "Masuf Travel - Лечение и Тур в Нафталан"
        settings.hero_badge_uz = "OZARBAYJON • GASHALTI HEALTH NAFTALAN 5*"
        settings.hero_badge_ru = "АЗЕРБАЙДЖАН • GASHALTI HEALTH NAFTALAN 5*"
        settings.hero_title_uz = "Ota-onangizga ham sayohat ham davolanish imkoniyatini hadya qiling"
        settings.hero_title_ru = "Подарите родителям возможность путешествия и лечения"
        settings.hero_subtitle_uz = "Naftalan sanatoriyasida malakali shifokorlar va zamonaviy texnologiyalar asosida yuqori sifatli davolanish, 5* qulaylik va Ozarbayjon bo'ylab ajoyib ekskursiyalar!"
        settings.hero_subtitle_ru = "Высококачественное лечение в санатории Нафталан с опытными врачами и современными технологиями, 5* комфорт и незабываемые экскурсии по Азербайджану!"
        settings.hero_media_type = 'image'
        settings.flight_dates_uz = "08.10.2026 (7 kecha 8 kun)"
        settings.flight_dates_ru = "08.10.2026 (7 ночей 8 дней)"
        settings.tour_price = "1350$"
        settings.hotel_name_uz = "5* mehmonxona - Gashalti Health Naftalan"
        settings.hotel_name_ru = "5* отель - Gashalti Health Naftalan"
        settings.phone_number = "+998994111151"
        settings.phone_number_2 = "+998974111151"
        settings.operator_name = "Abduqodir"
        settings.telegram_url = "https://t.me/khalilov1999"
        settings.instagram_url = "https://www.instagram.com/masuftravel?stkn=MWlpN2J2NXJ0d2dpaA=="
        settings.location_url = "https://yandex.ru/maps/-/CTxuVNMr"
        settings.whatsapp_url = ""

        settings.about_text_uz = (
            "Naftalan sanatoriyasida malakali shifokorlar va zamonaviy texnologiyalar asosida davolanish qo'llaniladi. "
            "Sizning ota-onangiz va yaqinlaringiz uchun shifobaxsh neft vannalari, to'liq tibbiy ko'rik, 5 yulduzli qulaylik "
            "hamda Boku, Qabala va Nohur ko'li bo'ylab go'zal sayohatlar taqdim etiladi."
        )
        settings.about_text_ru = (
            "В санатории Нафталан проводится лечение на основе квалифицированных врачей и современных технологий. "
            "Для ваших родителей и близких предоставляются целебные нафталановые ванны, полный медицинский осмотр, "
            "5-звездочный комфорт и прекрасные экскурсии по Баку, Габале и озеру Нохур."
        )

        # Agar hero image bo'lmasa yaratamiz
        if not settings.hero_image:
            hero_file = generate_sample_image("Gashalti Health Naftalan 5* & Sanatorium", 1920, 1080, (15, 60, 95))
            settings.hero_image.save("hero_default.jpg", hero_file, save=False)

        settings.save()
        self.stdout.write(self.style.SUCCESS("SiteSettings ma'lumotlari muvaffaqiyatli saqlandi."))

        # 4. Qanday kasalliklar uchun (Diseases)
        diseases_data = [
            {
                "title_uz": "Boʻgʻim va suyak kasalliklari (artroz, artrit, radikulit)",
                "title_ru": "Заболевания суставов и костей (артроз, артрит, радикулит)",
                "icon": "fas fa-bone",
                "description_uz": "Bo'g'imlardagi og'riqlarni kamaytirish, harakatchanlikni tiklash va yallig'lanishni bartaraf etishda dunyoga mashhur tabiiy Naftalan moyi eng samarali vositadir.",
                "description_ru": "Всемирно известная нафталановая нефть эффективно снимает боли в суставах, восстанавливает подвижность и устраняет воспаления.",
                "order": 1
            },
            {
                "title_uz": "Asab tizimi muammolari",
                "title_ru": "Заболевания нервной системы",
                "icon": "fas fa-brain",
                "description_uz": "Nevrit, nevralgiya, uyqusizlik, surunkali charchoq va stress oqibatlarini bartaraf etish, asab tolalari faoliyatini normallashtirish.",
                "description_ru": "Устранение невритов, невралгии, бессонницы, хронической усталости и последствий стресса, нормализация работы нервной системы.",
                "order": 2
            },
            {
                "title_uz": "Ginekologik va urologik kasalliklar",
                "title_ru": "Гинекологические и урологические заболевания",
                "icon": "fas fa-user-md",
                "description_uz": "Surunkali shamollashlar, bepushtlik profilaktikasi, prostatit va boshqa urologik hamda ginekologik a'zolar kasalliklarini kompleks davolash.",
                "description_ru": "Комплексное лечение хронических воспалений, профилактика бесплодия, простатита и других урологических и гинекологических заболеваний.",
                "order": 3
            },
            {
                "title_uz": "Teri kasalliklari (psoriaz, ekzema)",
                "title_ru": "Кожные заболевания (псориаз, экзема)",
                "icon": "fas fa-allergies",
                "description_uz": "Psoriaz, ekzema, neyrodermit va teri quruqligi muammolarini tabiiy Naftalan vannalari bilan xavfsiz va samarali bartaraf etish.",
                "description_ru": "Безопасное и эффективное устранение псориаза, экземы, нейродермита и сухости кожи с помощью нафталановых ванн.",
                "order": 4
            },
            {
                "title_uz": "Teri osti qon aylanishi buzilishi",
                "title_ru": "Нарушения периферического кровообращения",
                "icon": "fas fa-heartbeat",
                "description_uz": "Qon tomirlari tonusini oshirish, mikrosirkulyatsiyani yaxshilash va periferik qon aylanish tizimini tiklash.",
                "description_ru": "Повышение тонуса сосудов, улучшение микроциркуляции и восстановление периферической кровеносной системы.",
                "order": 5
            },
        ]

        Disease.objects.all().delete()
        for item in diseases_data:
            Disease.objects.create(
                title_uz=item["title_uz"],
                title_ru=item["title_ru"],
                icon=item["icon"],
                description_uz=item["description_uz"],
                description_ru=item["description_ru"],
                order=item["order"],
                is_active=True
            )
        self.stdout.write(self.style.SUCCESS("Kasalliklar ro'yxati (5 ta) UZ va RU tillarida saqlandi."))

        # 5. Narx ichiga kiruvchi sayohat xizmatlari (TourFeature)
        features_data = [
            {"title_uz": "5* mehmonxona - Gashalti Health Naftalan", "title_ru": "5* отель - Gashalti Health Naftalan", "icon": "fas fa-hotel", "highlight": True, "order": 1},
            {"title_uz": "3 mahal diet taomlar (Shved stoli)", "title_ru": "3-х разовое диетическое питание (Шведский стол)", "icon": "fas fa-utensils", "highlight": False, "order": 2},
            {"title_uz": "8 kunlik to'liq dam olish va hordiq", "title_ru": "8 дней полноценного отдыха и оздоровления", "icon": "fas fa-calendar-alt", "highlight": False, "order": 3},
            {"title_uz": "Standart - to'liq davolanish dasturi", "title_ru": "Стандартный - полный пакет лечебных процедур", "icon": "fas fa-heart", "highlight": True, "order": 4},
            {"title_uz": "Komfort zamonaviy avtobus xizmati", "title_ru": "Комфортабельный современный автобус", "icon": "fas fa-bus", "highlight": False, "order": 5},
            {"title_uz": "Naftalan va Gabala tog'i, Nohur ko'li, Tufandag' sayohati", "title_ru": "Экскурсии по Нафталану, гора Габала, озеро Нохур, Туфандаг", "icon": "fas fa-mountain", "highlight": True, "order": 6},
            {"title_uz": "Tog' osma yo'li (Kanat) to'lovi kiritilgan", "title_ru": "Канатная дорога (билет включен)", "icon": "fas fa-tram", "highlight": False, "order": 7},
            {"title_uz": "Baku shahri bo'ylab umumiy sayohat va ekskursiya", "title_ru": "Обзорная экскурсия по городу Баку", "icon": "fas fa-city", "highlight": True, "order": 8},
            {"title_uz": "Avtobusda yengil taomlanish (Lunch box)", "title_ru": "Легкий перекус в автобусе (Lunch box)", "icon": "fas fa-box-open", "highlight": False, "order": 9},
            {"title_uz": "Safar davomida sizning ota-onangiz bilan malakali yo'lboshchi birga boradi", "title_ru": "На протяжении всей поездки родителей сопровождает опытный гид", "icon": "fas fa-user-tie", "highlight": True, "order": 10},
        ]

        TourFeature.objects.all().delete()
        for item in features_data:
            TourFeature.objects.create(
                title_uz=item["title_uz"],
                title_ru=item["title_ru"],
                icon=item["icon"],
                highlight=item["highlight"],
                order=item["order"],
                is_active=True
            )
        self.stdout.write(self.style.SUCCESS("Sayohat xususiyatlari (10 ta) UZ va RU tillarida saqlandi."))

        # 6. Davolanish dasturi toifalari va ro'yxati (TreatmentCategory & TreatmentItem)
        categories_data = [
            {
                "title_uz": "📝 Shifokor qabuli",
                "title_ru": "📝 Приемы врачей",
                "icon": "fas fa-file-medical-alt",
                "order": 1,
                "items": [
                    {"uz": "1. Davolovchi shifokorning dastlabki qabuli", "ru": "1. Первичный прием лечащего врача"},
                    {"uz": "2. Davolovchi shifokorga vizitatsiya (muntazam nazorat)", "ru": "2. Регулярные визиты и наблюдение лечащего врача"},
                    {"uz": "3. Davolovchi shifokorning yakunlovchi qabuli va tavsiyalari", "ru": "3. Заключительный прием и рекомендации лечащего врача"},
                ]
            },
            {
                "title_uz": "💉 Laboratoriya tahlillari",
                "title_ru": "💉 Лабораторные анализы",
                "icon": "fas fa-vial",
                "order": 2,
                "items": [
                    {"uz": "4. Qonning klinik tahlili", "ru": "4. Клинический анализ крови"},
                    {"uz": "5. Qonda glyukoza miqdorini aniqlash (biokimyoviy tahlil)", "ru": "5. Определение уровня глюкозы в крови"},
                    {"uz": "6. Siydikning klinik tahlili", "ru": "6. Клинический анализ мочи"},
                ]
            },
            {
                "title_uz": "🩻 Diagnostika tekshiruvlari",
                "title_ru": "🩻 Диагностические обследования",
                "icon": "fas fa-x-ray",
                "order": 3,
                "items": [
                    {"uz": "7. Tinch holatdagi elektrokardiografiya (EKG)", "ru": "7. Электрокардиография в покое (ЭКГ)"},
                    {"uz": "8. Qorin bo'shlig'i a'zolarining UZIsi", "ru": "8. УЗИ органов брюшной полости"},
                ]
            },
            {
                "title_uz": "👨‍⚕️ Maxsus mutaxassislar qabuli va maslahati",
                "title_ru": "👨‍⚕️ Прием и консультации профильных специалистов",
                "icon": "fas fa-user-md",
                "order": 4,
                "items": [
                    {"uz": "9. Dietolog yoki stomatolog qabuli", "ru": "9. Прием диетолога или стоматолога"},
                    {"uz": "10. Urolog yoki ginekolog qabuli", "ru": "10. Прием уролога или гинеколога"},
                    {"uz": "11. Fizioterapevt yoki nevropatolog qabuli", "ru": "11. Прием физиотерапевта или невропатолога"},
                    {"uz": "12. Otorinolaringolog (LOR) qabuli", "ru": "12. Прием оториноларинголога (ЛОР)"},
                    {"uz": "13. Kardiolog qabuli", "ru": "13. Прием кардиолога"},
                ]
            },
            {
                "title_uz": "🔗 Davolash turlari va muolajalar",
                "title_ru": "🔗 Лечебные процедуры",
                "icon": "fas fa-spa",
                "order": 5,
                "items": [
                    {"uz": "1. Naftalan vannalari (Shifobaxsh Naftalan nefti)", "ru": "1. Нафталановые ванны (Целебная нафталановая нефть)"},
                    {"uz": "2. Yod-brom vannalari yoki fitovannalar", "ru": "2. Йодобромные ванны или фитованны"},
                    {"uz": "3. Infraqizil nurlar bilan davolash", "ru": "3. Инфракрасная терапия"},
                    {"uz": "4. Qisqa to'lqinli diatermiya", "ru": "4. Коротковолновая диатермия"},
                    {"uz": "5. Magnitoterapiya", "ru": "5. Магнитотерапия"},
                    {"uz": "6. Elektroterapiya", "ru": "6. Электротерапия"},
                    {"uz": "7. Amplipuls terapiya", "ru": "7. Амплипульстерапия"},
                    {"uz": "8. Lazer terapiya", "ru": "8. Лазеротерапия"},
                    {"uz": "9. Darsonvalizatsiya", "ru": "9. Дарсонвализация"},
                    {"uz": "10. Fonoforez", "ru": "10. Фонофорез"},
                ]
            },
        ]

        TreatmentCategory.objects.all().delete()
        for cat_info in categories_data:
            cat = TreatmentCategory.objects.create(
                title_uz=cat_info["title_uz"],
                title_ru=cat_info["title_ru"],
                icon=cat_info["icon"],
                order=cat_info["order"],
                is_active=True
            )
            # Itemlarni qo'shish
            for idx, item_data in enumerate(cat_info["items"], 1):
                TreatmentItem.objects.create(
                    category=cat,
                    name_uz=item_data["uz"],
                    name_ru=item_data["ru"],
                    order=idx,
                    is_active=True
                )
        self.stdout.write(self.style.SUCCESS("Davolanish toifalari va barcha 23 ta muolajalar UZ va RU tillarida saqlandi."))

        # 7. Galereya rasmlari va videolari (sample)
        if not GalleryPhoto.objects.exists():
            gallery_samples = [
                ("Gashalti Health Naftalan 5* Mehmonxona", "5* Отель Gashalti Health Naftalan", "hotel", 1, (24, 75, 110), "image"),
                ("Shifobaxsh Naftalan Moyi Vannasi", "Лечебные нафталановые ванны", "treatment", 2, (18, 50, 70), "image"),
                ("Qabala tog'lari va Tufandag' Kanat", "Горы Габала и канатная дорога Туфандаг", "nature", 3, (30, 90, 70), "image"),
                ("Nohur ko'li bo'ylab go'zal sayohat", "Живописная экскурсия на озеро Нохур", "nature", 4, (20, 80, 100), "image"),
                ("Fizioterapiya va Reabilitatsiya markazi", "Центр физиотерапии и реабилитации", "treatment", 5, (25, 65, 120), "image"),
                ("Baku shahri bo'ylab unutilmas sayohat", "Незабываемая экскурсия по Баку", "nature", 6, (40, 70, 90), "image"),
            ]
            for title_uz, title_ru, cat, order, color, m_type in gallery_samples:
                img_file = generate_sample_image(f"{title_uz}", 800, 600, color)
                photo = GalleryPhoto(
                    title_uz=title_uz, 
                    title_ru=title_ru, 
                    media_type=m_type, 
                    category=cat, 
                    order=order, 
                    is_active=True
                )
                photo.image.save(f"sample_{order}.jpg", img_file, save=True)
            self.stdout.write(self.style.SUCCESS("Galereya rasmlari yaratildi."))

        # 8. Test Leadlar (Videodagi 5 ta ariza)
        if Lead.objects.count() < 5:
            Lead.objects.all().delete()
            sample_leads = [
                {
                    "name": "Jasurbek",
                    "phone": "+998 (99) 893-55-54",
                    "message": "",
                    "source": "landing_form",
                    "status": "new",
                },
                {
                    "name": "Jasurbek",
                    "phone": "+998 (99) 893-55-54",
                    "message": "",
                    "source": "landing_form",
                    "status": "new",
                },
                {
                    "name": "Muzaffar Xamidov",
                    "phone": "+998 (99) 890-11-12",
                    "message": "Ota-onam uchun 2 kishilik sayohat haqida ma'lumot bering",
                    "source": "landing_form",
                    "status": "new",
                },
                {
                    "name": "Bekzod Rahimov",
                    "phone": "+998901234567",
                    "message": "Ozarbayjon Naftalan sayohati haqida ma'lumot bering",
                    "source": "landing_form",
                    "status": "new",
                },
                {
                    "name": "Sardor Rahimqulov",
                    "phone": "+998901234567",
                    "message": "Ota-onam uchun 2 kishilik sayohat va davolanish paketini bilmoqchi edim",
                    "source": "landing_form",
                    "status": "new",
                },
            ]
            for l_data in sample_leads:
                Lead.objects.create(
                    name=l_data["name"],
                    phone=l_data["phone"],
                    message=l_data["message"],
                    source=l_data["source"],
                    status=l_data["status"],
                )
            self.stdout.write(self.style.SUCCESS("Videodagi 5 ta namunaviy lead yaratildi."))

        self.stdout.write(self.style.SUCCESS("Barcha boshlang'ich ma'lumotlar muvaffaqiyatli tayyorlandi!"))
