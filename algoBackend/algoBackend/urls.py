from django.contrib import admin
from django.urls import path, include

from bilan.views import BilanViewset
from alm.views import BondsViewset, BondPortofolioViewset
from backoffice.views import AdminBondViewSet
from backoffice.views import AdminBondList

from customer_loans.views import LoansViewSet
from eib.views import EIBViewset
from pib.views import PIBViewset
from refi.views import RefiViewset
from dat.views import DATViewset
from op_retrait.views import OPRetraitViewset
from op_injection.views import OPInjectionViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'bilan', BilanViewset, basename='bilan')

router.register(r'bond', BondsViewset, basename='bond')
router.register(r'bond_portofolio', BondPortofolioViewset, basename='bond_portofolio')

router.register(r'eib', EIBViewset, basename='eib')
router.register(r'pib', PIBViewset, basename='pib')
router.register(r'dat', DATViewset, basename='dat')

router.register(r'refi', RefiViewset, basename='refi')
router.register(r'backoffice', AdminBondViewSet, basename='backoffice')
router.register(r'op_retrait', OPRetraitViewset, basename='op_retrait')
router.register(r'op_injection', OPInjectionViewSet, basename='op_injection')
router.register(r'customer_loan', LoansViewSet, basename='customer_loan')

# urlpatterns = router.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/admin-bonds/', AdminBondList.as_view(), name='admin_bond_list'),
    path('api/v1/auth/', include("accounts.urls")),
    path('api/v1/auth/', include('social_accounts.urls'))
]
