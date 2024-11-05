from netbox.views import generic
from netbox_vault import forms, models, tables
import requests
from dcim.models import Device
from utilities.views import ViewTab, register_model_view
from django.conf import settings

@register_model_view(Device, "EnvTech")
class VaultView(generic.ObjectView):
	"""
	Display a selected Vault
	"""
	tab = ViewTab(
		label='EnvTech',
		permission="dcim.view_device"
	)
	queryset = models.Vault.objects.all()
	table = tables.VaultTable
	template_name = "vault/vault.html"

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
