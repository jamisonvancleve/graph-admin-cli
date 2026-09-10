variable "resource_group_name" {
  type        = string
  description = "Name of the resource group"
}

variable "location" {
  type        = string
  description = "Azure region for resources"
}

variable "tags" {
  type        = map(string)
  default     = {}
  description = "Resource tags"
}