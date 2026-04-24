output "app_server_sg_id" {
  value = aws_security_group.app_server.id
}

output "jenkins_sg_id" {
  value = aws_security_group.jenkins.id
}

output "rds_sg_id" {
  value = aws_security_group.rds.id
}

output "elasticache_sg_id" {
  value = aws_security_group.elasticache_sg.id
}