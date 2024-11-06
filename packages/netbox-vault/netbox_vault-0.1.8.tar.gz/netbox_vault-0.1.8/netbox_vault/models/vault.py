from django.contrib.postgres.fields import ArrayField
from django.db import models
from netbox.models import NetBoxModel
from dcim.models import Device
from django.urls import reverse
import requests
from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager

class Vault(NetBoxModel):
	PrsID = models.IntegerField()
	device = models.OneToOneField(Device, on_delete=models.CASCADE, related_name='vault')

	class Meta:
		ordering = ('pk',)

	def __str__(self):
		return str(self.PrsID)

	def get_absolute_url(self):
		return reverse('plugins:netbox_vault:vault', args=[self.pk])

	def save(self, *args, **kwargs):
		device = self.get_device()
		if device is None:
			raise ValidationError(f"No device found with PrsID: {self.PrsID}")
		self.device = device
		super().save(*args, **kwargs)

	def get_device(self):
		try:
			return Device.objects.get(custom_field_data__PrsID=str(self.PrsID))
		except Device.DoesNotExist:
			return None

	def get_data(self):
		prsID = str(self.PrsID)
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
		
	def get_csl_env(self):
		data = self.get_data()
		if data is None:
			raise ValueError("Failed to retrieve data; 'get_data' returned None.")
		for entry in data:
			if entry.get('EnvRef1') == 'admin' and entry.get('DesignationID') == 'CSL':
				return entry.get('EnvRef2')
		self.set_csl_env()
			
	def set_csl_env(self):
		passwd = BaseUserManager().make_random_password(12)

	def get_loc_env(self):
		data = self.get_data()
		if data is None:
			raise ValueError("Failed to retrieve data; 'getData' returned None.")
		for entry in data:
			if entry.get('EnvRef1') == 'ipline' and entry.get('DesignationID') == 'LOC':
				return entry.get('EnvRef2')

	def set_loc_env(self):
		passwd = BaseUserManager().make_random_password(24)