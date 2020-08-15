from django.urls import path
from .views import *


urlpatterns = [
    path('giris/', LoginView.as_view()),
    path('cikis/', LogoutView.as_view()),
]