from datetime import datetime
from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import SwapOperation, SwapProposition
from .serializers import SwapOperationSerializer, SwapOperationCreateSerializer, SwapPropositionSerializer, SwapPropositionCreateSerializer

class SwapOperationViewSet(viewsets.ModelViewSet):
    
    def get_queryset(self):
        return SwapOperation.objects.filter(deleted=False)
    
    def get_serializer_class(self):
        return SwapOperationCreateSerializer if self.action == 'create' else SwapOperationSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], url_path='my_swap_operations', url_name='my_swap_operations')
    def my_swap_operations(self, request):
        operations = SwapOperation.objects.filter(user=request.user)
        serializer = SwapOperationSerializer(operations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class SwapPropositionViewset(viewsets.ModelViewSet):

    def get_queryset(self):
        return SwapProposition.objects.filter(deleted=False)
    
    def get_serializer_class(self):
        return SwapPropositionCreateSerializer if self.action == 'create' else SwapPropositionSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], url_path='my_swap_propositions', url_name='my_swap_propositions')
    def my_swap_propositions(self, request):
        propositions = SwapProposition.objects.filter(user=request.user)
        serializer = SwapPropositionSerializer(propositions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], url_path='reject_swap_proposition', url_name='reject_swap_proposition')
    def reject_swap_proposition(self, request, pk=None):
        proposition = self.get_object()
        proposition.status = 'R'
        proposition.save()

        serializer = SwapPropositionSerializer(proposition)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], url_path='accept_swap_proposition', url_name='accept_swap_proposition')
    def accept_swap_proposition(self, request, pk=None):
        proposition = self.get_object()
        proposition.status = 'A'
        proposition.accepted_date = datetime.date.today()
        proposition.save()

        serializer = SwapPropositionSerializer(proposition)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
