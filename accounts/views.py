
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.views.generic.base import ContextMixin
from django.utils.decorators import method_decorator

from django.http import JsonResponse

from .models import Account as User

from random import randint


# Create your views here.
class SettingsView(TemplateView):
    template_name = 'accounts/settings.html'


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('accounts:settings')
        return render(request, 'accounts/register.html', {'failed': kwargs.get('failed')})

    def post(self, request, *args, **kwargs):
        if request.POST.get('password_1') == request.POST.get('password_2'):
            user = User.objects.create_user(
                username=request.POST.get('username'),
                email=request.POST.get('email'),
                password=request.POST.get('password_2'),
            )
            user.save()
            login(request, user)
            return redirect('accounts:settings')
        return self.get(request, failed=True)


class LoginView(View):
    def get(self, request, failed=False, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('accounts:settings')
        return render(request, "accounts/login.html", {'failed': True} if failed else {})

    def post(self, request, *args, **kwargs):
        user = authenticate(
            request=request,
            username=request.POST.get('username'),
            password=request.POST.get('password'),
        )
        if not user:
            return self.get(request=request, failed=True, *args, **kwargs)
        login(request, user)
        return redirect('store:homepage')


class ChangeView(View):
    @login_required
    def change_password(request, *args, **kwargs):
        if request.method == 'GET':
            return render(request, 'accounts/change_password.html')
        elif request.method == 'POST':
            if check_password(request.POST.get('password_old'), request.user.password):
                request.user.set_password(request.POST.get('password_new'))
                return redirect('accounts:settings')

    @login_required
    def change_email(request, *args, **kwargs):
        if request.method == 'GET':
            render(request, 'accounts/change_email.html')
        elif request.method == 'POST':
            if check_password(request.POST.get('password_old'), request.user.password):
                request.user.set_password(request.POST.get('password_new'))
                return redirect('accounts:settings')

    @login_required
    def delete(request, *args, **kwargs):
        request.user.delete()
        logout(request)
        return redirect('store:homepage')


class ForgotPasswordView(View):
    confirmation = f'{randint(100_000_000, 999_999_999)}'

    def get(self, request, *args, **kwargs):

        return JsonResponse({'success': True})

    def post(self, request, *args, **kwargs):
        if request.POST.get('confirmation') == self.confirmation:
            render(request, 'accounts/forgot_password.html')


@login_required
def logoutView(request, *args, **kwargs):
    logout(request)
    return redirect('store:homepage')
