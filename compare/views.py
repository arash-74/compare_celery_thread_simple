from django.contrib import messages
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.views import PasswordResetView
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from time import time
from threading import Thread
from django.urls import reverse_lazy
from celery import shared_task
from compare.forms import SignInForm, ResetForm
from compare.models import User
from core import settings


# Create your views here.
def signin_view(request):
    form = None
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            form.save()
    if request.method == 'GET':
        form = SignInForm()
    context = {'form': form}
    return render(request, 'html/signin.html', context)


class MyPasswordResetView(PasswordResetView):
    template_name = 'html/password_reset_form.html'
    success_url = reverse_lazy('compare:reset-done')

    def form_valid(self, form):
        start = time()
        response = super().form_valid(form)
        end = time()
        messages.info(self.request, f' simple {end - start:.2f}')
        return response


def thread_password_reset(request):
    form = None
    if request.method == 'POST':
        start = time()
        form = ResetForm(request.POST)
        if form.is_valid():
            user = User.objects.get(email=form.cleaned_data['email'])
            token = PasswordResetTokenGenerator().make_token(request.user).split('-')
            url = f'{request.scheme}://{request.get_host()}/password-reset/conform/{token[0]}/{token[1]}'

            email = EmailMessage(
                body=url,
                to=[user.email],
            )
            task = Thread(target=email.send, kwargs={'fail_silently': False})
            task.start()
            end = time()
            messages.info(request, f' multi thread {end - start:.2f}')
            tp = 'thread'
            return redirect('compare:reset-done')
    if request.method == 'GET':
        form = ResetForm()
    context = {'form': form}
    return render(request, 'html/password_reset_form.html', context)

@shared_task
def send_email(url,email):
    email = EmailMessage(
        body=url,
        to=[email],
    )
    email.send()
def celery_password_reset(request):
    form = None
    if request.method == 'POST':
        start = time()
        form = ResetForm(request.POST)
        if form.is_valid():
            user = User.objects.get(email=form.cleaned_data['email'])
            token = PasswordResetTokenGenerator().make_token(request.user).split('-')
            url = f'{request.scheme}://{request.get_host()}/password-reset/conform/{token[0]}/{token[1]}'

            send_email.delay(url,user.email)
            end = time()
            messages.info(request, f' celery {end - start:.2f}')
            return redirect('compare:reset-done')
    if request.method == 'GET':
        form = ResetForm()
    context = {'form': form}
    return render(request, 'html/password_reset_form.html', context)
