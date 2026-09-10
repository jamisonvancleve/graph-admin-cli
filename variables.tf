variable "location" {
  type        = string
  default     = "eastus"
  description = "The target Azure region for resources."
}

variable "environment" {
  type        = string
  default     = "dev"
  description = "Environment identifier used for tags and naming."
}

variable "resource_group_name" {
  type        = string
  default     = "rg-graph-admin-cli-dev"
  description = "Name of the main workload resource group for graph-admin-cli."
}