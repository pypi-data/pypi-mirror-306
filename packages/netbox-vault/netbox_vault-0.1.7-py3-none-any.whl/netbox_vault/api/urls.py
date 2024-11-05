from netbox.api.routers import NetBoxRouter
from . import views

app_name = 'netbox_vault'

router = NetBoxRouter()
router.register('vault', views.VaultViewSet)

urlpatterns = router.urls