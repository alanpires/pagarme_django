from django.urls import path
from .views import PayableView

urlpatterns = [
    path('payables/', PayableView.as_view())
]
