from django.urls import path
from .views import LoginView, AccountView

urlpatterns = [
    path('accounts/', AccountView.as_view()),
    path('login/', LoginView.as_view())
]