from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import AdminBond
from .serializers import AdminBondSerializer

class AdminBondViewSet(viewsets.ModelViewSet):
    queryset = AdminBond.objects.all()
    serializer_class = AdminBondSerializer


class AdminBondList(APIView):
    def get(self, request, format=None):
        try:
            isins = AdminBond.objects.values_list('isin', flat=True)
            return Response(isins, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)