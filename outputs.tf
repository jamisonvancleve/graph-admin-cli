output "resource_group_name" {
  value       = azurerm_resource_group.rg.name
  description = "The name of the provisioned resource group."
}

output "virtual_network_id" {
  value       = azurerm_virtual_network.vnet.id
  description = "The resource ID of the Virtual Network."
}

output "subnet_id" {
  value       = azurerm_subnet.subnet.id
  description = "The resource ID of the application Subnet."
}