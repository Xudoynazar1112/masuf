from django import forms
from .models import (
    SiteSettings, Disease, TourFeature, 
    TreatmentCategory, TreatmentItem, Lead, GalleryPhoto
)


class LeadForm(forms.ModelForm):
    """Landing sahifadagi operator bilan bog'lanish formasi"""
    class Meta:
        model = Lead
        fields = ['name', 'phone', 'message', 'source']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control form-input',
                'placeholder': 'Ismingizni kiriting...',
                'required': 'required',
                'id': 'lead_name'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control form-input',
                'placeholder': '+998 (__) ___-__-__',
                'required': 'required',
                'id': 'lead_phone'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control form-input',
                'placeholder': 'Qo\'shimcha savol yoki istaklaringiz (ixtiyoriy)...',
                'rows': 3,
                'id': 'lead_message'
            }),
            'source': forms.HiddenInput(attrs={'value': 'landing_form', 'id': 'lead_source'})
        }


class SiteSettingsForm(forms.ModelForm):
    """Menejer dashboardida landing page sozlamalarini tahrirlash formasi (UZ va RU)"""
    class Meta:
        model = SiteSettings
        fields = [
            'site_title_uz', 'site_title_ru',
            'hero_badge_uz', 'hero_badge_ru',
            'hero_title_uz', 'hero_title_ru',
            'hero_subtitle_uz', 'hero_subtitle_ru',
            'about_text_uz', 'about_text_ru',
            'flight_dates_uz', 'flight_dates_ru',
            'hotel_name_uz', 'hotel_name_ru',
            'tour_price',
            'phone_number', 'phone_number_2', 'operator_name',
            'telegram_url', 'instagram_url', 'location_url', 'whatsapp_url',
            'hero_media_type', 'hero_image', 'hero_video', 'hero_video_url'
        ]
        widgets = {
            'site_title_uz': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masuf Travel - Naftalan...'}),
            'site_title_ru': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masuf Travel - Лечение в Нафталане...'}),
            'hero_badge_uz': forms.TextInput(attrs={'class': 'form-control'}),
            'hero_badge_ru': forms.TextInput(attrs={'class': 'form-control'}),
            'hero_title_uz': forms.TextInput(attrs={'class': 'form-control'}),
            'hero_title_ru': forms.TextInput(attrs={'class': 'form-control'}),
            'hero_subtitle_uz': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'hero_subtitle_ru': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'about_text_uz': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'about_text_ru': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'flight_dates_uz': forms.TextInput(attrs={'class': 'form-control'}),
            'flight_dates_ru': forms.TextInput(attrs={'class': 'form-control'}),
            'hotel_name_uz': forms.TextInput(attrs={'class': 'form-control'}),
            'hotel_name_ru': forms.TextInput(attrs={'class': 'form-control'}),
            'tour_price': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+998919686886'}),
            'phone_number_2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+998974111151'}),
            'operator_name': forms.TextInput(attrs={'class': 'form-control'}),
            'telegram_url': forms.TextInput(attrs={'class': 'form-control'}),
            'instagram_url': forms.TextInput(attrs={'class': 'form-control'}),
            'location_url': forms.TextInput(attrs={'class': 'form-control'}),
            'whatsapp_url': forms.TextInput(attrs={'class': 'form-control'}),
            'hero_media_type': forms.Select(attrs={'class': 'form-select', 'id': 'hero_media_type_select'}),
            'hero_image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'hero_video': forms.FileInput(attrs={'class': 'form-control', 'accept': 'video/*'}),
            'hero_video_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
        }


class DiseaseForm(forms.ModelForm):
    class Meta:
        model = Disease
        fields = ['title_uz', 'title_ru', 'icon', 'description_uz', 'description_ru', 'order', 'is_active']
        widgets = {
            'title_uz': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Boʻgʻim va suyak kasalliklari'}),
            'title_ru': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Заболевания суставов и костей'}),
            'icon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'fas fa-bone'}),
            'description_uz': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'description_ru': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class TourFeatureForm(forms.ModelForm):
    class Meta:
        model = TourFeature
        fields = ['title_uz', 'title_ru', 'icon', 'highlight', 'order', 'is_active']
        widgets = {
            'title_uz': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Aviachipta (borish-kelish)'}),
            'title_ru': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Авиабилеты (в обе стороны)'}),
            'icon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'fas fa-plane-departure'}),
            'highlight': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class TreatmentCategoryForm(forms.ModelForm):
    class Meta:
        model = TreatmentCategory
        fields = ['title_uz', 'title_ru', 'icon', 'order', 'is_active']
        widgets = {
            'title_uz': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Shifokor qabullari'}),
            'title_ru': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Приемы врачей'}),
            'icon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'fas fa-user-md'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class TreatmentItemForm(forms.ModelForm):
    class Meta:
        model = TreatmentItem
        fields = ['category', 'name_uz', 'name_ru', 'description_uz', 'description_ru', 'order', 'is_active']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'name_uz': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Terapevt ko\'rigi'}),
            'name_ru': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Осмотр терапевта'}),
            'description_uz': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'description_ru': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class LeadUpdateForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['status', 'operator_notes']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'operator_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Mijoz bilan muloqot xulosasi yoki keyingi qadamlar...'}),
        }


class GalleryPhotoForm(forms.ModelForm):
    """Galereya uchun rasm yoki video yuklash formasi (Hajm cheklovlari bilan)"""
    class Meta:
        model = GalleryPhoto
        fields = [
            'title_uz', 'title_ru', 'media_type', 
            'image', 'video', 'video_url', 
            'category', 'order', 'is_active'
        ]
        widgets = {
            'title_uz': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masalan: 5* Mehmonxona va Sanatoriya binosi'}),
            'title_ru': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: Здание отеля и санатория 5*'}),
            'media_type': forms.Select(attrs={'class': 'form-select', 'id': 'gallery_media_type_select'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*', 'id': 'gallery_image_input'}),
            'video': forms.FileInput(attrs={'class': 'form-control', 'accept': 'video/mp4,video/webm,video/ogg,video/quicktime', 'id': 'gallery_video_input'}),
            'video_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://www.youtube.com/... yoki video linki', 'id': 'gallery_video_url_input'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        media_type = cleaned_data.get('media_type')
        image = cleaned_data.get('image')
        video = cleaned_data.get('video')
        video_url = cleaned_data.get('video_url')

        if media_type == 'image':
            if not image and not (self.instance and self.instance.image):
                raise forms.ValidationError("Iltimos, rasm faylini tanlang (Maksimal hajm: 10 MB).")
        elif media_type == 'video':
            if not video and not (self.instance and self.instance.video):
                raise forms.ValidationError("Iltimos, video faylini tanlang (Maksimal hajm: 50 MB).")
        elif media_type == 'video_url':
            if not video_url and not (self.instance and self.instance.video_url):
                raise forms.ValidationError("Iltimos, video URL havolasini kiriting.")

        return cleaned_data


