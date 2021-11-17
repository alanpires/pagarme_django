from django.urls import path
from .views import FeeGenericView

urlpatterns = [
    path('fee/', FeeGenericView.as_view())
]