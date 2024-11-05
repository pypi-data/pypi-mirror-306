from netbox.forms import NetBoxModelForm
from netbox_vault import models
from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

class VaultForm(NetBoxModelForm):
    PrsID = forms.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(9999999)
        ],
        required=True
    )

    class Meta:
        model = models.Vault
        fields = ('PrsID', 'tags')