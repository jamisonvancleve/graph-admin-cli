output "acr_login_server" {
  value       = azurerm_container_registry.acr.login_server
  description = "The login server URL for ACR"
}

output "acr_name" {
  value       = azurerm_container_registry.acr.name
  description = "The container registry name"
}