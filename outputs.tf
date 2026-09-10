output "resource_group_name" {
  description = "The name of the resource group."
  value       = module.networking.resource_group_name
}

output "subnet_id" {
  description = "The ID of the application subnet."
  value       = module.networking.subnet_id
}

output "acr_login_server" {
  description = "The URL used to log into the container registry."
  value       = module.registry.acr_login_server
}

output "acr_name" {
  description = "The name of the container registry."
  value       = module.registry.acr_name
}