from fee.serializers import FeeSerializer
from django.shortcuts import render
from rest_framework import generics
from .models import Fee
from .serializers import FeeSerializer


class FeeGenericView(generics.ListCreateAPIView):
    queryset = Fee.objects.all()
    serializer_class = FeeSerializer