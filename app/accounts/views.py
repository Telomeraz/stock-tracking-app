from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/panel/')
        else:
            return render(request, 'accounts/login.html')
    
    def post(self, request):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            next_url = request.GET.get('next', '/panel/')
            return redirect(next_url)
        else:
            return redirect('/hesaplar/giris/')


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('/hesaplar/giris/')
