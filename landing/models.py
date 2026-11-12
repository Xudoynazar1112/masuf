from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


def validate_image_file_size(file):
    max_size = 10 * 1024 * 1024  # 10 MB
    if file and hasattr(file, 'size') and file.size > max_size:
        raise ValidationError(_("Rasm fayl hajmi 10 MB dan oshmasligi kerak (Maksimal ruxsat: 10MB)."))


def validate_video_file_size(file):
    max_size = 50 * 1024 * 1024  # 50 MB
    if file and hasattr(file, 'size') and file.size > max_size:
        raise ValidationError(_("Video fayl hajmi 50 MB dan oshmasligi kerak (Maksimal ruxsat: 50MB)."))


class SiteSettings(models.Model):
    """Landing sahifasining bosh sozlamalari, Hero qismi va asosiy kontaktlar (O'zbek va Rus tillarida)"""
    MEDIA_TYPE_CHOICES = [
        ('image', 'Rasm (Hero Image)'),
        ('video', 'Video (Hero Video)'),
    ]

    site_title_uz = models.CharField(
        max_length=255, 
        default="Masuf Travel - Naftalan Davolanish & Sayohat Dasturi",
        verbose_name=_("Sayt sarlavhasi (UZ)")
    )
    site_title_ru = models.CharField(
        max_length=255, 
        default="Masuf Travel - Лечение и Тур в Нафталан",
        verbose_name=_("Sayt sarlavhasi (RU)")
    )
    hero_badge_uz = models.CharField(
        max_length=150, 
        default="OZARBAYJON • GASHALTI HEALTH NAFTALAN 5*",
        verbose_name=_("Hero nishoni (UZ)")
    )
    hero_badge_ru = models.CharField(
        max_length=150, 
        default="АЗЕРБАЙДЖАН • GASHALTI HEALTH NAFTALAN 5*",
        verbose_name=_("Hero nishoni (RU)")
    )
    hero_title_uz = models.CharField(
        max_length=300, 
        default="Ota-onangizga ham sayohat ham davolanish imkoniyatini hadya qiling",
        verbose_name=_("Hero sarlavhasi (UZ)")
    )
    hero_title_ru = models.CharField(
        max_length=300, 
        default="Подарите родителям возможность путешествия и лечения",
        verbose_name=_("Hero sarlavhasi (RU)")
    )
    hero_subtitle_uz = models.TextField(
        default="Naftalan sanatoriyasida malakali shifokorlar va zamonaviy texnologiyalar asosida shifobaxsh neft va fizioterapiya orqali davolaning.",
        verbose_name=_("Hero tavsifi (UZ)")
    )
    hero_subtitle_ru = models.TextField(
        default="В санатории Нафталан проводится лечение на основе квалифицированных врачей и современных технологий с использованием целебной нафталановой нефти и физиотерапии.",
        verbose_name=_("Hero tavsifi (RU)")
    )
    hero_media_type = models.CharField(
        max_length=10, 
        choices=MEDIA_TYPE_CHOICES, 
        default='image',
        verbose_name=_("Hero media turi (Rasm yoki Video)")
    )
    hero_image = models.ImageField(
        upload_to='hero/', 
        blank=True, 
        null=True,
        verbose_name=_("Hero rasmi")
    )
    hero_video = models.FileField(
        upload_to='hero_videos/', 
        blank=True, 
        null=True,
        verbose_name=_("Hero video fayli (MP4)")
    )
    hero_video_url = models.URLField(
        blank=True, 
        null=True,
        help_text="Video linki (YouTube, Vimeo yoki to'g'ridan-to'g'ri MP4 havolasi)",
        verbose_name=_("Hero video URL havolasi")
    )
    flight_dates_uz = models.CharField(
        max_length=150, 
        default="08.10.2026 (7 kecha 8 kun)",
        verbose_name=_("Uchish sanasi (UZ)")
    )
    flight_dates_ru = models.CharField(
        max_length=150, 
        default="08.10.2026 (7 ночей 8 дней)",
        verbose_name=_("Uchish sanasi (RU)")
    )
    tour_price = models.CharField(
        max_length=50, 
        default="1350$",
        verbose_name=_("Sayohat narxi")
    )
    hotel_name_uz = models.CharField(
        max_length=200, 
        default="5* mehmonxona - Gashalti Health Naftalan",
        verbose_name=_("Mehmonxona (UZ)")
    )
    hotel_name_ru = models.CharField(
        max_length=200, 
        default="5* отель - Gashalti Health Naftalan",
        verbose_name=_("Mehmonxona (RU)")
    )
    phone_number = models.CharField(
        max_length=50, 
        default="+998919686886",
        verbose_name=_("Asosiy telefon raqami (1)")
    )
    phone_number_2 = models.CharField(
        max_length=50, 
        default="+998974111151",
        blank=True,
        verbose_name=_("Qo'shimcha telefon raqami (2)")
    )
    operator_name = models.CharField(
        max_length=100, 
        default="Abduqodir",
        verbose_name=_("Mas'ul operator ismi")
    )
    telegram_url = models.CharField(
        max_length=255, 
        default="https://t.me/khalilov1999",
        verbose_name=_("Telegram havolasi")
    )
    instagram_url = models.CharField(
        max_length=500, 
        default="https://www.instagram.com/masuftravel?stkn=MWlpN2J2NXJ0d2dpaA==",
        verbose_name=_("Instagram havolasi")
    )
    location_url = models.CharField(
        max_length=500, 
        default="https://yandex.ru/maps/-/CTxuVNMr",
        verbose_name=_("Lokatsiya / Xarita havolasi")
    )
    whatsapp_url = models.CharField(
        max_length=255, 
        default="",
        blank=True,
        verbose_name=_("WhatsApp havolasi")
    )
    about_text_uz = models.TextField(
        default="Naftalan sanatoriyasida malakali shifokorlar va zamonaviy texnologiyalar asosida yuqori sifatli davolanish xizmatlari taqdim etiladi. Ota-onangiz sog'lig'i va dam olishi uchun barcha sharoitlar yaratilgan.",
        verbose_name=_("Dastur haqida matn (UZ)")
    )
    about_text_ru = models.TextField(
        default="В санатории Нафталан предоставляются высококачественные лечебные услуги на основе квалифицированных врачей и современных технологий. Созданы все условия для здоровья и отдыха ваших родителей.",
        verbose_name=_("Dastur haqida matn (RU)")
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Faol"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("So'nggi yangilanish"))

    class Meta:
        verbose_name = _("Sayt sozlamalari va Bosh ma'lumotlar")
        verbose_name_plural = _("Sayt sozlamalari va Bosh ma'lumotlar")

    def __str__(self):
        return f"{self.site_title_uz} ({self.flight_dates_uz})"

    @classmethod
    def get_settings(cls):
        settings, _ = cls.objects.get_or_create(id=1)
        return settings

    # Helper getters for active language
    @property
    def flight_dates(self):
        return self.flight_dates_uz

    def get_title(self, lang='uz'):
        return self.site_title_ru if lang == 'ru' else self.site_title_uz

    def get_hero_title(self, lang='uz'):
        return self.hero_title_ru if lang == 'ru' else self.hero_title_uz

    def get_hero_badge(self, lang='uz'):
        return self.hero_badge_ru if lang == 'ru' else self.hero_badge_uz

    def get_hero_subtitle(self, lang='uz'):
        return self.hero_subtitle_ru if lang == 'ru' else self.hero_subtitle_uz

    def get_flight_dates(self, lang='uz'):
        return self.flight_dates_ru if lang == 'ru' else self.flight_dates_uz

    def get_hotel_name(self, lang='uz'):
        return self.hotel_name_ru if lang == 'ru' else self.hotel_name_uz

    def get_about_text(self, lang='uz'):
        return self.about_text_ru if lang == 'ru' else self.about_text_uz


class Disease(models.Model):
    """Qanday kasalliklar uchun davolanish bo'limi (UZ va RU)"""
    title_uz = models.CharField(max_length=255, default="", verbose_name=_("Kasallik guruhi nomi (UZ)"))
    title_ru = models.CharField(max_length=255, default="", verbose_name=_("Kasallik guruhi nomi (RU)"), blank=True)
    icon = models.CharField(
        max_length=100, 
        default="fas fa-heartbeat", 
        help_text="FontAwesome icon (masalan: fas fa-bone, fas fa-brain, fas fa-user-md)",
        verbose_name=_("Ikonka")
    )
    description_uz = models.TextField(blank=True, default="", verbose_name=_("Tavsif (UZ)"))
    description_ru = models.TextField(blank=True, default="", verbose_name=_("Tavsif (RU)"))
    order = models.PositiveIntegerField(default=0, verbose_name=_("Tartib raqami"))
    is_active = models.BooleanField(default=True, verbose_name=_("Faol"))

    class Meta:
        ordering = ['order', 'id']
        verbose_name = _("Kasallik turi")
        verbose_name_plural = _("Qanday kasalliklar uchun")

    def __str__(self):
        return self.title_uz or self.title_ru or f"Disease #{self.id}"

    def get_title(self, lang='uz'):
        return (self.title_ru if lang == 'ru' and self.title_ru else self.title_uz)

    def get_description(self, lang='uz'):
        return (self.description_ru if lang == 'ru' and self.description_ru else self.description_uz)


class TourFeature(models.Model):
    """Narx ichiga kiruvchi sayohat va mehmonxona xizmatlari (UZ va RU)"""
    title_uz = models.CharField(max_length=255, default="", verbose_name=_("Xizmat nomi (UZ)"))
    title_ru = models.CharField(max_length=255, default="", verbose_name=_("Xizmat nomi (RU)"), blank=True)
    icon = models.CharField(
        max_length=100, 
        default="fas fa-check-circle",
        help_text="FontAwesome ikonka (masalan: fas fa-hotel, fas fa-utensils, fas fa-bus)",
        verbose_name=_("Ikonka")
    )
    highlight = models.BooleanField(default=False, verbose_name=_("Alohida ajratish"))
    order = models.PositiveIntegerField(default=0, verbose_name=_("Tartib raqami"))
    is_active = models.BooleanField(default=True, verbose_name=_("Faol"))

    class Meta:
        ordering = ['order', 'id']
        verbose_name = _("Sayohat xizmati")
        verbose_name_plural = _("1-punkt: Sayohat xizmatlari")

    def __str__(self):
        return self.title_uz or self.title_ru or f"Feature #{self.id}"

    def get_title(self, lang='uz'):
        return (self.title_ru if lang == 'ru' and self.title_ru else self.title_uz)


class TreatmentCategory(models.Model):
    """Davolanish dasturi toifalari (Shifokor qabuli, Laboratoriya, Diagnostika, Mutaxassislar, Muolajalar)"""
    title_uz = models.CharField(max_length=255, default="", verbose_name=_("Kategoriya nomi (UZ)"))
    title_ru = models.CharField(max_length=255, default="", verbose_name=_("Kategoriya nomi (RU)"), blank=True)
    icon = models.CharField(max_length=100, default="fas fa-stethoscope", verbose_name=_("Ikonka"))
    order = models.PositiveIntegerField(default=0, verbose_name=_("Tartib raqami"))
    is_active = models.BooleanField(default=True, verbose_name=_("Faol"))

    class Meta:
        ordering = ['order', 'id']
        verbose_name = _("Davolanish kategoriyasi")
        verbose_name_plural = _("Davolanish kategoriyalari")

    def __str__(self):
        return self.title_uz or self.title_ru or f"Category #{self.id}"

    def get_title(self, lang='uz'):
        return (self.title_ru if lang == 'ru' and self.title_ru else self.title_uz)


class TreatmentItem(models.Model):
    """Kategoriya ichidagi har bir muolaja yoki tibbiy xizmat"""
    category = models.ForeignKey(
        TreatmentCategory, 
        on_delete=models.CASCADE, 
        related_name='items',
        verbose_name=_("Kategoriya")
    )
    name_uz = models.CharField(max_length=255, default="", verbose_name=_("Xizmat / Muolaja nomi (UZ)"))
    name_ru = models.CharField(max_length=255, default="", verbose_name=_("Xizmat / Muolaja nomi (RU)"), blank=True)
    description_uz = models.TextField(blank=True, default="", verbose_name=_("Qo'shimcha izoh (UZ)"))
    description_ru = models.TextField(blank=True, default="", verbose_name=_("Qo'shimcha izoh (RU)"))
    order = models.PositiveIntegerField(default=0, verbose_name=_("Tartib raqami"))
    is_active = models.BooleanField(default=True, verbose_name=_("Faol"))

    class Meta:
        ordering = ['order', 'id']
        verbose_name = _("Davolanish muolajasi")
        verbose_name_plural = _("Davolanish muolajalari")

    def __str__(self):
        return f"{self.category.title_uz}: {self.name_uz}"

    def get_name(self, lang='uz'):
        return (self.name_ru if lang == 'ru' and self.name_ru else self.name_uz)


class Lead(models.Model):
    """Operator bilan bog'lanish uchun qoldirilgan arizalar (Lidlar)"""
    STATUS_CHOICES = [
        ('new', '🆕 Yangi'),
        ('contacted', '📞 Bog\'lanildi'),
        ('in_progress', '⏳ O\'rganilmoqda / Suhbatda'),
        ('sold', '✅ Sotuv amalga oshdi'),
        ('cancelled', '❌ Bekor qilindi'),
    ]

    name = models.CharField(max_length=150, verbose_name=_("Mijoz ismi"))
    phone = models.CharField(max_length=50, verbose_name=_("Telefon raqami"))
    message = models.TextField(blank=True, verbose_name=_("Mijoz xabari / Istagi"))
    source = models.CharField(max_length=100, default="landing_form", verbose_name=_("Manba"))
    status = models.CharField(
        max_length=30, 
        choices=STATUS_CHOICES, 
        default='new',
        verbose_name=_("Ariza holati")
    )
    operator_notes = models.TextField(
        blank=True, 
        verbose_name=_("Operator izohi / Eslatmalari")
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Qoldirilgan sana"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Yangilangan sana"))

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Mijoz arizasi (Lead)")
        verbose_name_plural = _("Mijozlar arizalari (Leadlar)")

    def __str__(self):
        return f"{self.name} - {self.phone} ({self.get_status_display()})"


class GalleryPhoto(models.Model):
    """Sanatoriya, mehmonxona va ekskursiya fotosuratlari va videolari (3-punkt)"""
    MEDIA_TYPE_CHOICES = [
        ('image', 'Rasm (Photo)'),
        ('video', 'Video fayl (MP4/WebM)'),
        ('video_url', 'Video havola (YouTube / Havola)'),
    ]

    CATEGORY_CHOICES = [
        ('all', 'Barchasi / Umumiy'),
        ('hotel', 'Mehmonxona & Xonalar'),
        ('treatment', 'Davolanish & Tibbiyot'),
        ('nature', 'Ekskursiya & Tabiat'),
    ]

    title_uz = models.CharField(max_length=200, default="", verbose_name=_("Media sarlavhasi (UZ)"))
    title_ru = models.CharField(max_length=200, default="", blank=True, verbose_name=_("Media sarlavhasi (RU)"))
    media_type = models.CharField(
        max_length=15, 
        choices=MEDIA_TYPE_CHOICES, 
        default='image',
        verbose_name=_("Media turi (Rasm yoki Video)")
    )
    image = models.ImageField(
        upload_to='gallery/images/', 
        blank=True, 
        null=True,
        validators=[validate_image_file_size],
        verbose_name=_("Rasm fayli (Maks 10MB)")
    )
    video = models.FileField(
        upload_to='gallery/videos/', 
        blank=True, 
        null=True,
        validators=[validate_video_file_size],
        verbose_name=_("Video fayli (Maks 50MB)")
    )
    video_url = models.URLField(
        blank=True, 
        null=True,
        verbose_name=_("Video URL havolasi")
    )
    category = models.CharField(
        max_length=50, 
        choices=CATEGORY_CHOICES, 
        default='hotel',
        verbose_name=_("Bo'lim / Kategoriya")
    )
    order = models.PositiveIntegerField(default=0, verbose_name=_("Tartib raqami"))
    is_active = models.BooleanField(default=True, verbose_name=_("Faol"))
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name=_("Qo'shilgan sana"))

    class Meta:
        ordering = ['order', 'id']
        verbose_name = _("Galereya media fayli (Rasm/Video)")
        verbose_name_plural = _("3-punkt: Rasmlar va Videolar")

    def __str__(self):
        return self.title_uz or self.title_ru or f"Media #{self.id}"

    def get_title(self, lang='uz'):
        return (self.title_ru if lang == 'ru' and self.title_ru else self.title_uz)
