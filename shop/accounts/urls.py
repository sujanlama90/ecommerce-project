from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views #alising
urlpatterns = [
    path('log_in/',log_in.as_view(),name='log_in'),
    path('register/',register.as_view(),name='register'),
    path('log_out/',log_out,name='log_out'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='account/password_reset.html',html_email_template_name='account/mail.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'), name='password_reset_complete'),

    # profile
    path('profile_dashboard/',profile_dashboard,name='profile_dashboard'),
    path('profile/',profile,name='profile'),
    # email verification
     path('send-verification-email/',send_verification_email,name='send_verification_email'),
    path('verify-email/<uuid:token>/', verify_email,name='verify_email'),
]
