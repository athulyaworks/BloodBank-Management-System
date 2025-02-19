from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Main Pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('review/', views.review, name='review'),

    # Authentication URLs
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Donor URLs
    path('donor/signup/', views.DonorSignUpView.as_view(), name='donor_signup'),
    path('donor/login/', views.donor_login, name='donor_login'),
    path('donor/dashboard/', views.donor_dashboard, name='donor_dashboard'),

    # Patient URLs
    path('patient/signup/', views.PatientSignUpView.as_view(), name='patient_signup'),
    path('patient/login/', views.patient_login, name='patient_login'),
    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('patient/request-blood/', views.request_blood, name='request_blood'),

    # Authority URLs
    path('authority/signup/', views.AuthoritySignUpView.as_view(), name='authority_signup'),
    path('authority-login/', views.authority_login, name='authority_login'),
    path('authority-dashboard/', views.authority_dashboard, name='authority_dashboard'),
    path('authority/approve-donor/<int:donor_id>/', views.approve_donor, name='approve_donor'),
    path('authority/approve-request/<int:request_id>/', views.approve_patient_request, name='approve_patient_request'),

    # Blood Inventory URLs
    path('inventory/', views.blood_inventory, name='blood_inventory'),
    path('inventory/update/', views.update_inventory, name='update_inventory'),

    # Profile Management
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/change-password/', auth_views.PasswordChangeView.as_view(
        template_name='registration/password_change.html',
        success_url='password_change_done'
    ), name='password_change'),
    path('profile/change-password/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='registration/password_change_done.html'
    ), name='password_change_done'),

    # Password Reset URLs
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset.html'
    ), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),

    # Additional Features
    path('search/', views.search_blood, name='search_blood'),
    path('donation-history/', views.donation_history, name='donation_history'),
    path('request-history/', views.request_history, name='request_history'),
    path('logout/',views.logout_view, name='logout'),
]
