import django_tables2 as tables

from netbox.tables import NetBoxTable, ChoiceFieldColumn
from .models import Vault

class VaultTable(NetBoxTable):
    pk = tables.Column(
        linkify=True
    )
    device = tables.Column(
        linkify=True
    )

    class Meta(NetBoxTable.Meta):
        model = Vault
        fields = ('pk', 'id', 'device', 'actions')
        default_columns = ('pk', 'device', 'default_action')