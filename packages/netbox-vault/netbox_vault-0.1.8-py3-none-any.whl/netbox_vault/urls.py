from django.urls import path
from . import views
from netbox.views.generic import ObjectChangeLogView
from netbox_vault import models

urlpatterns = (
	path('vault/', views.VaultListView.as_view(), name='vault_list'),
	path('vault/add/', views.VaultEditView.as_view(), name='vault_add'),
	path('vault/<int:pk>/', views.VaultView.as_view(), name='vault'),
	path('vault/<int:pk>/edit/', views.VaultEditView.as_view(), name='vault_edit'),
	path('vault/<int:pk>/delete/', views.VaultDeleteView.as_view(), name='vault_delete'),
    path('vault/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='vault_changelog', kwargs={
        'model': models.Vault
    }),
)