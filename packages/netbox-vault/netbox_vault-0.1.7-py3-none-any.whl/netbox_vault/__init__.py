from netbox.plugins import PluginConfig

class NetboxVaultConfig(PluginConfig):
    name = "netbox_vault"
    verbose_name = "Netbox Vault"
    description = "Netbox plugin to manage EnvTech between Vault, DW and Netbox"
    version = "0.1"
    author = "Arthur ASCEDU"
    author_email = "aascedu@student.42lyon.fr"
    base_url = "netbox-vault"
    min_version = "4.1.0"
    max_version = "4.1.99"

config = NetboxVaultConfig