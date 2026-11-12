from django.urls import path
from . import views

urlpatterns = [
    # Public Landing Page
    path('', views.landing_page, name='landing_page'),
    path('submit-lead/', views.submit_lead, name='submit_lead'),

    # Manager / User Custom Dashboard
    path('dashboard/', views.dashboard_home, name='dashboard_home'),
    path('dashboard/login/', views.dashboard_login_view, name='dashboard_login'),
    path('dashboard/logout/', views.dashboard_logout_view, name='dashboard_logout'),
    
    # Settings & Landing Page Content Editing
    path('dashboard/settings/', views.dashboard_settings_edit, name='dashboard_settings'),
    
    # Leads / Applications
    path('dashboard/leads/', views.dashboard_leads_list, name='dashboard_leads'),
    path('dashboard/leads/<int:pk>/', views.dashboard_lead_detail, name='dashboard_lead_detail'),
    path('dashboard/leads/<int:pk>/delete/', views.dashboard_lead_delete, name='dashboard_lead_delete'),
    
    # Diseases
    path('dashboard/diseases/', views.dashboard_diseases_list, name='dashboard_diseases'),
    path('dashboard/diseases/<int:pk>/edit/', views.dashboard_disease_edit, name='dashboard_disease_edit'),
    path('dashboard/diseases/<int:pk>/delete/', views.dashboard_disease_delete, name='dashboard_disease_delete'),
    
    # Treatments
    path('dashboard/treatments/', views.dashboard_treatments_list, name='dashboard_treatments'),
    path('dashboard/treatments/<int:pk>/edit/', views.dashboard_treatment_edit, name='dashboard_treatment_edit'),
    path('dashboard/treatments/<int:pk>/delete/', views.dashboard_treatment_delete, name='dashboard_treatment_delete'),
    
    # Tour Features
    path('dashboard/features/', views.dashboard_features_list, name='dashboard_features'),
    path('dashboard/features/<int:pk>/edit/', views.dashboard_feature_edit, name='dashboard_feature_edit'),
    path('dashboard/features/<int:pk>/delete/', views.dashboard_feature_delete, name='dashboard_feature_delete'),
    
    # Gallery (3-punkt: Rasmlar va Videolar)
    path('dashboard/gallery/', views.dashboard_gallery_list, name='dashboard_gallery'),
    path('dashboard/gallery/<int:pk>/edit/', views.dashboard_gallery_edit, name='dashboard_gallery_edit'),
    path('dashboard/gallery/<int:pk>/delete/', views.dashboard_gallery_delete, name='dashboard_gallery_delete'),
]

