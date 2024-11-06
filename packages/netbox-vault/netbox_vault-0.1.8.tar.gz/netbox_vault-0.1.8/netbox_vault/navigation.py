from netbox.plugins import PluginMenu, PluginMenuButton, PluginMenuItem

vault_menu_buttons = [
    PluginMenuButton(
        link='plugins:netbox_vault:vault_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
    )
]

vault_menu_items = (
	PluginMenuItem(
		link=f"plugins:netbox_vault:vault_list",
		link_text="Envtech",
		buttons=vault_menu_buttons
	),
)

menu = PluginMenu(
	label="Vault",
	groups=(("Vault", vault_menu_items),),
	icon_class="mdi mdi-checkbox-marked-circle-outline",
)