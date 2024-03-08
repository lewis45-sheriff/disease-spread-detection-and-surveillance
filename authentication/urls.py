from django.urls import path
from django.contrib.auth import views as auth_views
from authentication import views
from . import views


urlpatterns = [
    # Login view using custom login template
    path('login/', auth_views.LoginView.as_view(template_name='authentication/login.html'), name='login'),

    # Homepage view
    path('', views.homepage, name='homepage'),

    # Logout view
    path('logout/', views.as_view ,name='logout'),

    # Register view
    path('register/', views.register, name='register'),

    # Activate view
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    # Reset password views
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='authentication/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='authentication/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='authentication/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='authentication/password_reset_complete.html'), name='password_reset_complete'),

    # Paths for specific user types
    path('healthworker/', views.healthcare_worker_view, name='healthworker'),
    path('adminn/', views.admin_view, name='adminn'),
    path('predict/', views.predict_disease, name='predict_disease'),
    # Other 
    path('chat/<int:receiver_id>/', views.chat, name='chat'),
]


    

    



