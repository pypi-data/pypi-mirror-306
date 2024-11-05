from rest_framework import serializers

from netbox.api.serializers import NetBoxModelSerializer, WritableNestedSerializer
from ..models import Vault

class VaultSerializer(NetBoxModelSerializer):
	url = serializers.HyperlinkedIdentityField(
		view_name='plugins-api:netbox_vault-api:vault-detail'
	)

	class Meta:
		model = Vault
		fields = (
			'id', 'display', 'tags', 'custom_fields', 'created',
			'last_updated',
	    )