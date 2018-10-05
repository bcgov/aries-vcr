from rest_framework.routers import SimpleRouter
from api import views


router = SimpleRouter()

router.register(r'user', views.UserViewSet)
router.register(r'verifiableorgtype', views.VerifiableOrgTypeViewSet)
router.register(r'jurisdiction', views.JurisdictionViewSet)
router.register(r'verifiableorg', views.VerifiableOrgViewSet)
router.register(r'doingbusinessas', views.DoingBusinessAsViewSet)
router.register(r'inactiveclaimreason', views.InactiveClaimReasonViewSet)
router.register(r'issuerservice', views.IssuerServiceViewSet)
router.register(r'locationtype', views.LocationTypeViewSet)
router.register(r'location', views.LocationViewSet)
router.register(r'verifiableclaimtype', views.VerifiableClaimTypeViewSet)
router.register(r'verifiableclaim', views.VerifiableClaimViewSet)

urlpatterns = router.urls
