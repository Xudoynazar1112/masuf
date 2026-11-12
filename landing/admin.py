from django.contrib import admin
from django.utils.html import format_html
from .models import (
    SiteSettings, Disease, TourFeature, 
    TreatmentCategory, TreatmentItem, Lead, GalleryPhoto
)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_title_uz', 'site_title_ru', 'flight_dates_uz', 'tour_price', 'phone_number', 'phone_number_2', 'operator_name', 'hero_media_type', 'updated_at')
    fieldsets = (
        ("Asosiy Ma'lumotlar", {
            'fields': ('site_title_uz', 'site_title_ru', 'about_text_uz', 'about_text_ru', 'is_active')
        }),
        ("Hero Bo'limi (Eng yuqori qism)", {
            'fields': (
                'hero_badge_uz', 'hero_badge_ru', 'hero_title_uz', 'hero_title_ru', 'hero_subtitle_uz', 'hero_subtitle_ru', 
                'hero_media_type', 'hero_image', 'hero_video', 'hero_video_url'
            )
        }),
        ("Sayohat va Narx Ma'lumotlari", {
            'fields': ('flight_dates_uz', 'flight_dates_ru', 'tour_price', 'hotel_name_uz', 'hotel_name_ru')
        }),
        ("Aloqa va Operator", {
            'fields': ('phone_number', 'phone_number_2', 'operator_name', 'telegram_url', 'instagram_url', 'location_url', 'whatsapp_url')
        }),
    )

    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ('title_uz', 'title_ru', 'icon', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title_uz', 'title_ru', 'description_uz', 'description_ru')
    list_filter = ('is_active',)


@admin.register(TourFeature)
class TourFeatureAdmin(admin.ModelAdmin):
    list_display = ('title_uz', 'title_ru', 'icon', 'highlight', 'order', 'is_active')
    list_editable = ('highlight', 'order', 'is_active')
    search_fields = ('title_uz', 'title_ru')
    list_filter = ('highlight', 'is_active')


class TreatmentItemInline(admin.TabularInline):
    model = TreatmentItem
    extra = 1
    fields = ('name_uz', 'name_ru', 'description_uz', 'description_ru', 'order', 'is_active')


@admin.register(TreatmentCategory)
class TreatmentCategoryAdmin(admin.ModelAdmin):
    list_display = ('title_uz', 'title_ru', 'icon', 'items_count', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title_uz', 'title_ru')
    list_filter = ('is_active',)
    inlines = [TreatmentItemInline]

    def items_count(self, obj):
        return obj.items.count()
    items_count.short_description = "Muolajalar soni"


@admin.register(TreatmentItem)
class TreatmentItemAdmin(admin.ModelAdmin):
    list_display = ('name_uz', 'name_ru', 'category', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name_uz', 'name_ru', 'description_uz', 'description_ru')


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'colored_status', 'source', 'created_at', 'updated_at')
    list_filter = ('status', 'source', 'created_at')
    search_fields = ('name', 'phone', 'message', 'operator_notes')
    list_editable = ()
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ("Mijoz ma'lumotlari", {
            'fields': ('name', 'phone', 'message', 'source')
        }),
        ("Holat va Operator izohi", {
            'fields': ('status', 'operator_notes')
        }),
        ("Vaqt ko'rsatkichlari", {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def colored_status(self, obj):
        colors = {
            'new': '#2563eb',          # Ko'k
            'contacted': '#d97706',    # To'q sariq
            'in_progress': '#7c3aed',  # Binafsharang
            'sold': '#16a34a',         # Yashil
            'cancelled': '#dc2626',    # Qizil
        }
        color = colors.get(obj.status, '#64748b')
        return format_html(
            '<span style="background-color: {}; color: #fff; padding: 4px 10px; border-radius: 12px; font-weight: 600; font-size: 12px;">{}</span>',
            color,
            obj.get_status_display()
        )
    colored_status.short_description = "Holat"


@admin.register(GalleryPhoto)
class GalleryPhotoAdmin(admin.ModelAdmin):
    list_display = ('title_uz', 'title_ru', 'media_type', 'category', 'media_preview', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('media_type', 'category', 'is_active')
    search_fields = ('title_uz', 'title_ru')

    def media_preview(self, obj):
        if obj.media_type == 'image' and obj.image:
            return format_html('<img src="{}" style="width: 60px; height: 40px; object-fit: cover; border-radius: 4px;" />', obj.image.url)
        elif obj.media_type == 'video' and obj.video:
            return format_html('<span style="background: #e0f2fe; color: #0284c7; padding: 3px 8px; border-radius: 4px; font-weight: 600; font-size: 11px;">🎬 Video fayl</span>')
        elif obj.media_type == 'video_url':
            return format_html('<span style="background: #fef3c7; color: #b45309; padding: 3px 8px; border-radius: 4px; font-weight: 600; font-size: 11px;">🔗 Video havola</span>')
        return "Fayl yo'q"
    media_preview.short_description = "Ko'rinish"

