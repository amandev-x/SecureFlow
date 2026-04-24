output "app_server_public_ip" {
  description = "Public IP of app server (Kind cluster)"
  value       = aws_eip.app_server.public_ip
}

output "jenkins_public_ip" {
  description = "Public IP of Jenkins server"
  value       = aws_eip.jenkins.public_ip
}

output "app_server_id" {
  description = "Instance ID of app server"
  value       = aws_instance.app_server.id
}

output "jenkins_id" {
  description = "Instance ID of Jenkins server"
  value       = aws_instance.jenkins.id
}