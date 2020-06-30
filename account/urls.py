from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

app_name = "account"

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name="register"),
    path('edit/', views.edit_profile, name='edit'),
    path('about/', views.about, name='about'),
    path('test/', views.test, name='test'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name="password_reset"),
    path('password_reset/done/', auth_views.PasswordChangeDoneView.as_view(), name="password_reset_complete"),
    path('password_reset/done/', auth_views.PasswordChangeDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset/done', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('reset/done', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_done"),
    path('', views.dashboard, name="dashboard"),

]
