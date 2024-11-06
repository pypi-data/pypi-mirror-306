from netbox.views import generic
from netbox_vault import forms, models, tables
import requests
from dcim.models import Device
from utilities.views import ViewTab, register_model_view
from django.conf import settings
from django.shortcuts import get_object_or_404

@register_model_view(Device, name="EnvTech", path='vault')
class VaultView(generic.ObjectView):
	"""
	Display a selected Vault
	"""
	tab = ViewTab(
		label='EnvTech',
		badge=lambda obj: models.Vault.objects.filter(device=obj).count(),
		permission="dcim.view_device"
	)
	queryset = models.Vault.objects.all()
	table = tables.VaultTable
	template_name = "vault/vault.html"
	
	def get_object(self, **kwargs):
		if '/dcim/devices/' in self.request.path:
			device = get_object_or_404(Device, pk=self.kwargs['pk'])
			return get_object_or_404(models.Vault, device=device)
		elif '/plugins/netbox-vault/vault/' in self.request.path:
			return get_object_or_404(models.Vault, pk=self.kwargs['pk'])

	def get_extra_context(self, request, instance):
		context = {}
		context['prsID'] = instance.device.cf.get('PrsID')
		context['vault_data'] = self.getData(context['prsID'])
		return context

	def getData(self, prsID):
		url = 'https://vault.ipline.bur/middleware/ws_envtecs_mdp?PrsID=' + prsID
		try:
			response = requests.get(url,
									verify=False,
									cookies={"X-Vault-Token": settings.PLUGINS_CONFIG['netbox_vault']['VAULT_TOKEN']},)
			response.raise_for_status()
			return response.json()
		except requests.Timeout:
			print("Timeout")
			return None
		except requests.RequestException as e:
			print(f"Error fetching data: {e}")
			return None

class VaultListView(generic.ObjectListView):
	queryset = models.Vault.objects.all()
	table = tables.VaultTable

class VaultEditView(generic.ObjectEditView):
	queryset = models.Vault.objects.all()
	form = forms.VaultForm

class VaultDeleteView(generic.ObjectDeleteView):
	queryset = models.Vault.objects.all()
