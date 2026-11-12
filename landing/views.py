import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.utils import timezone
from .models import (
    SiteSettings, Disease, TourFeature, 
    TreatmentCategory, TreatmentItem, Lead, GalleryPhoto
)
from .forms import (
    LeadForm, SiteSettingsForm, DiseaseForm, TourFeatureForm,
    TreatmentCategoryForm, TreatmentItemForm, LeadUpdateForm, GalleryPhotoForm
)


# ==========================================
# 1. LANDING PAGE & PUBLIC VIEWS
# ==========================================

def landing_page(request):
    """Asosiy Landing Page ko'rinishi (O'zbek va Rus tillarida)"""
    lang = request.GET.get('lang')
    if lang in ['uz', 'ru']:
        request.session['lang'] = lang
    current_lang = request.session.get('lang', 'uz')

    settings = SiteSettings.get_settings()
    diseases = Disease.objects.filter(is_active=True).order_by('order', 'id')
    features = TourFeature.objects.filter(is_active=True).order_by('order', 'id')
    categories = TreatmentCategory.objects.filter(is_active=True).prefetch_related(
        'items'
    ).order_by('order', 'id')
    gallery = GalleryPhoto.objects.filter(is_active=True).order_by('order', 'id')
    form = LeadForm()

    context = {
        'settings': settings,
        'diseases': diseases,
        'features': features,
        'categories': categories,
        'gallery': gallery,
        'form': form,
        'current_lang': current_lang,
    }
    return render(request, 'landing/index.html', context)


def submit_lead(request):
    """Mijoz arizasini (Ism va telefon) qabul qilish (AJAX va standart POST)"""
    current_lang = request.session.get('lang', 'uz')

    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            lead = form.save()
            
            success_msg = (
                "Ваша заявка успешно принята! Наш оператор свяжется с вами в ближайшее время."
                if current_lang == 'ru'
                else "Arizangiz muvaffaqiyatli qabul qilindi! Tez orada operatorimiz siz bilan bog'lanadi."
            )

            # Agar AJAX so'rov bo'lsa
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.content_type == 'application/json':
                return JsonResponse({
                    'success': True,
                    'message': success_msg,
                    'lead_id': lead.id
                })
            
            messages.success(request, success_msg)
            return redirect('landing_page')
        else:
            error_msg = (
                "Пожалуйста, проверьте правильность введенного имени и номера телефона."
                if current_lang == 'ru'
                else "Iltimos, ism va telefon raqamingizni to'g'ri kiriting."
            )
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors,
                    'message': error_msg
                }, status=400)
            
            messages.error(request, error_msg)
            return redirect('landing_page')

    return redirect('landing_page')


# ==========================================
# 2. MANAGER / USER CUSTOM DASHBOARD
# ==========================================

def dashboard_login_view(request):
    """Menejer va admin uchun qulay kirish sahifasi"""
    if request.user.is_authenticated:
        return redirect('dashboard_home')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Xush kelibsiz, {user.username}!")
            next_url = request.GET.get('next', 'dashboard_home')
            return redirect(next_url)
        else:
            messages.error(request, "Foydalanuvchi nomi yoki parol noto'g'ri kiritildi.")
    else:
        form = AuthenticationForm()

    return render(request, 'auth/login.html', {'form': form})


def dashboard_logout_view(request):
    """Chiqish"""
    logout(request)
    messages.info(request, "Tizimdan muvaffaqiyatli chiqdingiz.")
    return redirect('dashboard_login')


@login_required
def dashboard_home(request):
    """Boshqaruv paneli bosh sahifasi (Statistika va umumiy ko'rinish)"""
    settings = SiteSettings.get_settings()
    
    # Statistikalar
    total_leads = Lead.objects.count()
    new_leads = Lead.objects.filter(status='new').count()
    contacted_leads = Lead.objects.filter(status='contacted').count()
    sold_leads = Lead.objects.filter(status='sold').count()

    # So'nggi 8 ta ariza
    recent_leads = Lead.objects.all().order_by('-created_at')[:8]

    # Umumiy kontent sonlari
    diseases_count = Disease.objects.count()
    treatments_count = TreatmentItem.objects.count()
    features_count = TourFeature.objects.count()
    gallery_count = GalleryPhoto.objects.count()

    context = {
        'settings': settings,
        'total_leads': total_leads,
        'new_leads': new_leads,
        'contacted_leads': contacted_leads,
        'sold_leads': sold_leads,
        'recent_leads': recent_leads,
        'diseases_count': diseases_count,
        'treatments_count': treatments_count,
        'features_count': features_count,
        'gallery_count': gallery_count,
        'active_menu': 'home',
    }
    return render(request, 'dashboard/index.html', context)


@login_required
def dashboard_settings_edit(request):
    """Landing sahifasining bosh matnlari, narxi, rasm/videosini tahrirlash"""
    settings = SiteSettings.get_settings()

    if request.method == 'POST':
        form = SiteSettingsForm(request.POST, request.FILES, instance=settings)
        if form.is_valid():
            form.save()
            messages.success(request, "Landing sahifasi ma'lumotlari muvaffaqiyatli yangilandi!")
            return redirect('dashboard_settings')
        else:
            messages.error(request, "Ma'lumotlarni saqlashda xatolik yuz berdi. Iltimos tekshiring.")
    else:
        form = SiteSettingsForm(instance=settings)

    context = {
        'settings': settings,
        'form': form,
        'active_menu': 'settings',
    }
    return render(request, 'dashboard/settings_edit.html', context)


@login_required
def dashboard_leads_list(request):
    """Arizalar (Leadlar) ro'yxati, filter va qidiruv"""
    status_filter = request.GET.get('status', '')
    query = request.GET.get('q', '')

    leads = Lead.objects.all().order_by('-created_at')

    if status_filter:
        leads = leads.filter(status=status_filter)

    if query:
        leads = leads.filter(
            Q(name__icontains=query) | 
            Q(phone__icontains=query) | 
            Q(message__icontains=query) | 
            Q(operator_notes__icontains=query)
        )

    status_choices = Lead.STATUS_CHOICES
    new_leads_count = Lead.objects.filter(status='new').count()

    context = {
        'leads': leads,
        'status_filter': status_filter,
        'query': query,
        'status_choices': status_choices,
        'new_leads_count': new_leads_count,
        'active_menu': 'leads',
    }
    return render(request, 'dashboard/leads_list.html', context)


@login_required
def dashboard_lead_detail(request, pk):
    """Bitta leadni ko'rish va holatini/izohini yangilash"""
    lead = get_object_or_404(Lead, pk=pk)

    if request.method == 'POST':
        form = LeadUpdateForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            messages.success(request, f"'{lead.name}' arizasi holati yangilandi!")
            return redirect('dashboard_leads')
    else:
        form = LeadUpdateForm(instance=lead)

    context = {
        'lead': lead,
        'form': form,
        'active_menu': 'leads',
    }
    return render(request, 'dashboard/lead_detail.html', context)


@login_required
def dashboard_lead_delete(request, pk):
    """Leadni o'chirish"""
    lead = get_object_or_404(Lead, pk=pk)
    if request.method == 'POST':
        lead.delete()
        messages.success(request, "Ariza muvaffaqiyatli o'chirildi.")
    return redirect('dashboard_leads')


@login_required
def dashboard_diseases_list(request):
    """Kasalliklar bo'limi boshqaruvi"""
    diseases = Disease.objects.all().order_by('order', 'id')
    form = DiseaseForm()

    if request.method == 'POST':
        form = DiseaseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Yangi kasallik turi qo'shildi!")
            return redirect('dashboard_diseases')

    context = {
        'diseases': diseases,
        'form': form,
        'active_menu': 'diseases',
    }
    return render(request, 'dashboard/disease_list.html', context)


@login_required
def dashboard_disease_edit(request, pk):
    """Kasallikni tahrirlash"""
    disease = get_object_or_404(Disease, pk=pk)
    if request.method == 'POST':
        form = DiseaseForm(request.POST, instance=disease)
        if form.is_valid():
            form.save()
            messages.success(request, "Kasallik ma'lumotlari yangilandi!")
            return redirect('dashboard_diseases')
    else:
        form = DiseaseForm(instance=disease)

    return render(request, 'dashboard/disease_edit.html', {'form': form, 'disease': disease, 'active_menu': 'diseases'})


@login_required
def dashboard_disease_delete(request, pk):
    disease = get_object_or_404(Disease, pk=pk)
    if request.method == 'POST':
        disease.delete()
        messages.success(request, "Kasallik o'chirildi.")
    return redirect('dashboard_diseases')


@login_required
def dashboard_treatments_list(request):
    """Davolanish toifalari va muolajalar boshqaruvi"""
    categories = TreatmentCategory.objects.prefetch_related('items').all().order_by('order', 'id')
    cat_form = TreatmentCategoryForm()
    item_form = TreatmentItemForm()

    if request.method == 'POST':
        if 'add_category' in request.POST:
            cat_form = TreatmentCategoryForm(request.POST)
            if cat_form.is_valid():
                cat_form.save()
                messages.success(request, "Yangi davolanish toifasi qo'shildi!")
                return redirect('dashboard_treatments')
        elif 'add_item' in request.POST:
            item_form = TreatmentItemForm(request.POST)
            if item_form.is_valid():
                item_form.save()
                messages.success(request, "Yangi muolaja/xizmat qo'shildi!")
                return redirect('dashboard_treatments')

    context = {
        'categories': categories,
        'cat_form': cat_form,
        'item_form': item_form,
        'active_menu': 'treatments',
    }
    return render(request, 'dashboard/treatment_list.html', context)


@login_required
def dashboard_treatment_edit(request, pk):
    """Muolajani tahrirlash"""
    item = get_object_or_404(TreatmentItem, pk=pk)
    if request.method == 'POST':
        form = TreatmentItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Muolaja muvaffaqiyatli yangilandi!")
            return redirect('dashboard_treatments')
    else:
        form = TreatmentItemForm(instance=item)

    return render(request, 'dashboard/treatment_edit.html', {'form': form, 'item': item, 'active_menu': 'treatments'})


@login_required
def dashboard_treatment_delete(request, pk):
    item = get_object_or_404(TreatmentItem, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, "Muolaja o'chirildi.")
    return redirect('dashboard_treatments')


@login_required
def dashboard_features_list(request):
    """Sayohat qulayliklari (Tour features) boshqaruvi"""
    features = TourFeature.objects.all().order_by('order', 'id')
    form = TourFeatureForm()

    if request.method == 'POST':
        form = TourFeatureForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Yangi xizmat qo'shildi!")
            return redirect('dashboard_features')

    context = {
        'features': features,
        'form': form,
        'active_menu': 'features',
    }
    return render(request, 'dashboard/feature_list.html', context)


@login_required
def dashboard_feature_edit(request, pk):
    feature = get_object_or_404(TourFeature, pk=pk)
    if request.method == 'POST':
        form = TourFeatureForm(request.POST, instance=feature)
        if form.is_valid():
            form.save()
            messages.success(request, "Xizmat yangilandi!")
            return redirect('dashboard_features')
    else:
        form = TourFeatureForm(instance=feature)
    return render(request, 'dashboard/feature_edit.html', {'form': form, 'feature': feature, 'active_menu': 'features'})


@login_required
def dashboard_feature_delete(request, pk):
    feature = get_object_or_404(TourFeature, pk=pk)
    if request.method == 'POST':
        feature.delete()
        messages.success(request, "Xizmat o'chirildi.")
    return redirect('dashboard_features')


@login_required
def dashboard_gallery_list(request):
    """3-punkt: Rasmlar va Videolar galereyasi boshqaruvi"""
    photos = GalleryPhoto.objects.all().order_by('order', 'id')
    form = GalleryPhotoForm()

    if request.method == 'POST':
        form = GalleryPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            media_item = form.save()
            type_label = "Video" if media_item.media_type in ['video', 'video_url'] else "Rasm"
            messages.success(request, f"Yangi {type_label} muvaffaqiyatli yuklandi!")
            return redirect('dashboard_gallery')
        else:
            messages.error(request, "Faylni yuklashda xatolik yuz berdi. Hajm va formatlarni tekshiring.")

    context = {
        'photos': photos,
        'form': form,
        'active_menu': 'gallery',
    }
    return render(request, 'dashboard/gallery_list.html', context)


@login_required
def dashboard_gallery_edit(request, pk):
    """Galereya media elementini tahrirlash"""
    photo = get_object_or_404(GalleryPhoto, pk=pk)
    if request.method == 'POST':
        form = GalleryPhotoForm(request.POST, request.FILES, instance=photo)
        if form.is_valid():
            form.save()
            messages.success(request, "Media ma'lumotlari muvaffaqiyatli yangilandi!")
            return redirect('dashboard_gallery')
        else:
            messages.error(request, "O'zgarishlarni saqlashda xatolik yuz berdi.")
    else:
        form = GalleryPhotoForm(instance=photo)

    return render(request, 'dashboard/gallery_edit.html', {
        'form': form,
        'photo': photo,
        'active_menu': 'gallery',
    })


@login_required
def dashboard_gallery_delete(request, pk):
    photo = get_object_or_404(GalleryPhoto, pk=pk)
    if request.method == 'POST':
        photo.delete()
        messages.success(request, "Media elementi o'chirildi.")
    return redirect('dashboard_gallery')

