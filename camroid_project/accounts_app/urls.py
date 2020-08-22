from django.urls import path

from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('register',views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('activate/<uidb64>/<token>', views.ActivateAccountView.as_view(), name='activate'),
    path('request-reset-link', views.RequestPasswordResetEmail.as_view(), name='request-password'),
    path('set-new-password/<uidb64>/<token>', views.CompletePasswordReset.as_view(), name='reset-user-password'),
]