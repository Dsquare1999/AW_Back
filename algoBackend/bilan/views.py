from django.shortcuts import render
from rest_framework import viewsets, status

from .models import Bilan
from .serializers import BilanSerializer, BilanListSerializer

# Create your views here.

class BilanViewset(viewsets.ModelViewSet):
    queryset = Bilan.objects.filter(deleted=False)
    serializer_class = BilanSerializer

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return BilanSerializer
        return BilanListSerializer
    

    def get_queryset(self):
        user = self.request.user
        queryset = Bilan.objects.filter(user=user, deleted=False)
        return queryset