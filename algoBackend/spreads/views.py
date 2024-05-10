from datetime import datetime
from rest_framework.response import Response

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from .models import SpreadOperation, SpreadProposition
from .serializers import SpreadOperationSerializer, SpreadOperationCreateSerializer, SpreadPropositionSerializer, SpreadPropositionCreateSerializer

# Create your views here.

class SpreadOperationViewSet(viewsets.ModelViewSet):
    
    def get_queryset(self):
        return SpreadOperation.objects.filter(deleted=False)
    
    def get_serializer_class(self):
        return SpreadOperationCreateSerializer if self.action == 'create' else SpreadOperationSerializer

    def create(self, request, *args, **kwargs):
        try:
            user = request.user
            request.data["user"] = user.id

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    @action(detail=False, methods=['get'], url_path='my_spread_operations', url_name='my_spread_operations')
    def my_operations(self, request):
        operations = SpreadOperation.objects.filter(user=request.user)
        serializer = SpreadOperationSerializer(operations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SpreadPropositionViewset(viewsets.ModelViewSet):
    def get_queryset(self):
        return SpreadProposition.objects.filter(deleted=False)
    
    def get_serializer_class(self):
        return SpreadPropositionCreateSerializer if self.action == 'create' else SpreadPropositionSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], url_path='my_spread_propositions', url_name='my_spread_propositions')
    def my_spread_propositions(self, request):
        propositions = SpreadProposition.objects.filter(user=request.user)
        serializer = SpreadPropositionSerializer(propositions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], url_path='reject_spread_proposition', url_name='reject_spread_proposition')
    def reject_spread_proposition(self, request, pk=None):
        proposition = self.get_object()
        proposition.status = 'R'
        proposition.save()

        serializer = SpreadPropositionSerializer(proposition)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], url_path='accept_spread_proposition', url_name='accept_spread_proposition')
    def accept_spread_proposition(self, request, pk=None):
        proposition = self.get_object()
        proposition.status = 'A'
        proposition.accepted_date = datetime.date.today()
        proposition.save()

        serializer = SpreadPropositionSerializer(proposition)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], url_path='confirm_spread_proposition', url_name='confirm_spread_proposition')
    def confirm_spread_proposition(self, request, pk=None):
        proposition = self.get_object()
        proposition.status = 'A'
        proposition.confirmation_date = datetime.date.today()
        proposition.save()

        serializer = SpreadPropositionSerializer(proposition)
        return Response(serializer.data, status=status.HTTP_200_OK)
