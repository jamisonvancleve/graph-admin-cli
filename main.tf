module "networking" {
  source              = "./modules/networking"
  resource_group_name = "rg-graph-admin-cli-dev"
  location            = "eastus"
  tags = {
    Environment = "dev"
    ManagedBy   = "Terraform"
  }
}

module "registry" {
  source              = "./modules/registry"
  acr_name            = "acrgraphadmincli2026"
  resource_group_name = module.networking.resource_group_name
  location            = module.networking.location
  tags = {
    Environment = "dev"
    ManagedBy   = "Terraform"
  }
}

# --- State Migration Blocks ---
moved {
  from = azurerm_resource_group.rg
  to   = module.networking.azurerm_resource_group.rg
}

moved {
  from = azurerm_virtual_network.vnet
  to   = module.networking.azurerm_virtual_network.vnet
}

moved {
  from = azurerm_subnet.subnet
  to   = module.networking.azurerm_subnet.subnet
}

moved {
  from = azurerm_container_registry.acr
  to   = module.registry.azurerm_container_registry.acr
}