from django.contrib.auth.forms import PasswordResetForm
from django.urls import path
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetConfirmView

from compare import views

app_name = 'compare'
urlpatterns = [
    path('signin', views.signin_view, name='signin'),
    path('password-reset-done', PasswordResetDoneView.as_view(template_name='html/password_reset_done.html'),
         name='reset-done'),
    path('password-reset/conform/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='html/password_reset_confirm.html'),
         name='reset_reset_conform'),
    path('simple-password-reset', views.MyPasswordResetView.as_view(), name='reset'),
    path('thread-password-reset', views.thread_password_reset, name='reset'),
    path('celery-password-reset', views.celery_password_reset, name='reset')
]
