variable "project_name" {
  type = string
}

variable "environment" {
  type = string
}

variable "service_names" {
  description = "List of service names to create ECR repos for"
  type        = list(string)
  default = [
    "api-gateway",
    "user-service",
    "product-service",
    "order-service",
    "notification-service"
  ]
}