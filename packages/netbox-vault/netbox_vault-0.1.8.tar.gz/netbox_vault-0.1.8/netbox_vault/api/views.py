from netbox.api.viewsets import NetBoxModelViewSet

from .. import  models
from .serializers import VaultSerializer

class VaultViewSet(NetBoxModelViewSet):
    queryset = models.Vault.objects.prefetch_related('tags')
    serializer_class = VaultSerializer