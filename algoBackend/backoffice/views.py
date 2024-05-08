from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from .models import AdminBond
from .serializers import AdminBondSerializer, AdminBondCreateSerializer

class AdminBondViewSet(viewsets.ModelViewSet):
    queryset = AdminBond.objects.filter(deleted=False)
    serializer_class = AdminBondSerializer


class AdminBondList(APIView):

    def get_serializer_class(self):
        return AdminBondCreateSerializer if self.action == 'create' else AdminBondSerializer
    
    def get(self, request, format=None):
        try:
            admin_bonds = AdminBond.objects.filter(deleted=False)
            serializer = AdminBondSerializer(admin_bonds, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'], url_path='isins', url_name='isins')
    def isins(self, request, format=None):
        try:
            isins = AdminBond.objects.values_list('isin', flat=True)
            return Response(isins, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)