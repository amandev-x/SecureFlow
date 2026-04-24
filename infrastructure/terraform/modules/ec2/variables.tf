variable "project_name" {
  type = string
}

variable "environment" {
  type = string
}

variable "app_instance_type" {
  description = "Instance type for app server"
  type        = string
  default     = "t3.small"
}

variable "jenkins_instance_type" {
  description = "Instance type for Jenkins server"
  type        = string
  default     = "t2.micro"
}

variable "public_subnet_id" {
  description = "Public subnet ID to launch instances in"
  type        = string
}

variable "app_server_sg_id" {
  description = "Security group ID for app server"
  type        = string
}

variable "jenkins_sg_id" {
  description = "Security group ID for Jenkins"
  type        = string
}

variable "key_name" {
  description = "EC2 key pair name for SSH access"
  type        = string
}