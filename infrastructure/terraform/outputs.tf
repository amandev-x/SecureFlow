output "app_server_public_ip" {
  value       = module.ec2.app_server_public_ip
  description = "Public ip of App Server"
}

output "jenkins_public_ip" {
  value       = module.ec2.jenkins_public_ip
  description = "Public ip of Jenkins UI"
}

output "rds_endpoint" {
  value       = module.rds.rds_endpoint
  description = "RDS PostgreSQL Endpoint"
}

output "rds_host" {
  value       = module.rds.rds_host
  description = "RDS host without port"
}

output "redis_url" {
  value       = module.elasticache.redis_url
  description = "Elasticache Redis URL"
}

output "ecr_repository_urls" {
  value       = module.ecr.repository_urls
  description = "ECR Repository URLs for every service"
}



