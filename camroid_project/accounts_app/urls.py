from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('register',views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('activate/<uidb64>/<token>', views.ActivateAccountView.as_view(), name='activate'),
    path('request-reset-link', views.RequestPasswordResetEmail.as_view(), name='request-password'),
    path('set-new-password/<uidb64>/<token>', views.CompletePasswordReset.as_view(), name='reset-user-password'),

    url(r'^check_email_exists/$', views.check_email_exists, name='check_email_exists'),
    
    url(r'^check_email_notexists/$', views.check_email_notexists, name='check_email_notexists'),
    url(r'^check_username_notexists/$', views.check_username_notexists, name='check_username_notexists'),
 
]