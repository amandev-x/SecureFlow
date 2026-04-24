resource "aws_security_group" "app_server" {
  name        = "${var.project_name}-app-server-sg"
  description = "Security group for app server"
  vpc_id      = var.vpc_id

  tags = {
    Name        = "${var.project_name}-app-server-sg"
    Environment = var.environment
  }
}

resource "aws_vpc_security_group_ingress_rule" "app_ssh_ingress" {
  security_group_id = aws_security_group.app_server.id
  cidr_ipv4         = var.my_ip
  ip_protocol       = "tcp"
  from_port         = 22
  to_port           = 22

  tags = {
    Name        = "${var.project_name}-app-ssh-ingress"
    Environment = var.environment
  }
}

resource "aws_vpc_security_group_ingress_rule" "api_gateway_ingress" {
  security_group_id = aws_security_group.app_server.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "tcp"
  from_port         = 8000
  to_port           = 8000

  tags = {
    Name        = "${var.project_name}-gateway-ingress"
    Environment = var.environment
  }
}

resource "aws_vpc_security_group_ingress_rule" "nginx_ingress" {
  security_group_id = aws_security_group.app_server.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "tcp"
  from_port         = 80
  to_port           = 80

  tags = {
    Name        = "${var.project_name}-nginx-ingress"
    Environment = var.environment
  }
}

resource "aws_vpc_security_group_ingress_rule" "https_ingress" {
  security_group_id = aws_security_group.app_server.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "tcp"
  from_port         = 443
  to_port           = 443

  tags = {
    Name        = "${var.project_name}-http-ingress"
    Environment = var.environment
  }
}

resource "aws_vpc_security_group_ingress_rule" "jenkins_to_app_ssh" {
  security_group_id = aws_security_group.app_server.id
  description       = "Allow SSH from Jenkins Server"
  ip_protocol       = "tcp"
  from_port         = 22
  to_port           = 22
  # This targets the Jenkins SG specifically:
  referenced_security_group_id = aws_security_group.jenkins.id

  tags = {
    Name        = "${var.project_name}-jenkins-to-app-ssh"
    Environment = var.environment
  }
}

resource "aws_vpc_security_group_egress_rule" "app-egress" {
  security_group_id = aws_security_group.app_server.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1"

  tags = {
    Name        = "${var.project_name}-app-outbound-egress"
    Environment = var.environment
  }
}

# ── Jenkins Server Security Group ─────────────────────────────────────────────
resource "aws_security_group" "jenkins" {
  name        = "${var.project_name}-jenkins-sg"
  description = "Security group for Jenkins server"
  vpc_id      = var.vpc_id

  tags = {
    Name        = "${var.project_name}-jenkins-sg"
    Environment = var.environment
  }
}

resource "aws_vpc_security_group_ingress_rule" "jenkins_ssh_ingress" {
  security_group_id = aws_security_group.jenkins.id
  ip_protocol       = "tcp"
  from_port         = 22
  to_port           = 22
  cidr_ipv4         = var.my_ip

  tags = {
    Name        = "${var.project_name}-jenkins-ssh-ingress"
    Environment = var.environment
  }
}

resource "aws_vpc_security_group_ingress_rule" "jenkins_ui" {
  security_group_id = aws_security_group.jenkins.id
  ip_protocol       = "tcp"
  from_port         = 8080
  to_port           = 8080
  cidr_ipv4         = "0.0.0.0/0"

  tags = {
    Name        = "${var.project_name}-jenkins-ui-ingress"
    Environment = var.environment
  }
}

resource "aws_vpc_security_group_egress_rule" "jenkins-egress" {
  security_group_id = aws_security_group.jenkins.id
  ip_protocol       = "-1"
  cidr_ipv4         = "0.0.0.0/0"

  tags = {
    Name        = "${var.project_name}-jenkins-outbound-egress"
    Environment = var.environment
  }
}

# ── RDS Security Group ────────────────────────────────────────────────────────

resource "aws_security_group" "rds" {
  name        = "${var.project_name}-rds-sg"
  description = "Security group for RDS"
  vpc_id      = var.vpc_id

  tags = {
    Name        = "${var.project_name}-rds-sg"
    Environment = var.environment
  }
}

resource "aws_vpc_security_group_ingress_rule" "rds_ingress" {
  security_group_id            = aws_security_group.rds.id
  description                  = "Traffic from only app server"
  ip_protocol                  = "tcp"
  from_port                    = 5432
  to_port                      = 5432
  referenced_security_group_id = aws_security_group.app_server.id

  tags = {
    Name        = "${var.project_name}-rds-ingress"
    Environment = var.environment
  }
}

resource "aws_vpc_security_group_egress_rule" "rds_egress" {
  security_group_id = aws_security_group.rds.id
  ip_protocol       = "-1"
  cidr_ipv4         = "0.0.0.0/0"

  tags = {
    Name        = "${var.project_name}-rds-egress"
    Environment = var.environment
  }
}

# ── ElastiCache Security Group ────────────────────────────────────────────────
resource "aws_security_group" "elasticache_sg" {
  name        = "${var.project_name}-elasticache-sg"
  description = "Security group for ElastiCache"
  vpc_id      = var.vpc_id

  tags = {
    Name        = "${var.project_name}-elasticache-sg"
    Environment = var.environment
  }
}

resource "aws_vpc_security_group_ingress_rule" "elasticache_ingress" {
  security_group_id            = aws_security_group.elasticache_sg.id
  ip_protocol                  = "tcp"
  from_port                    = 6379
  to_port                      = 6379
  referenced_security_group_id = aws_security_group.app_server.id

  tags = {
    Name        = "${var.project_name}-elasticache-ingress"
    Environment = var.environment
  }
}

resource "aws_vpc_security_group_egress_rule" "elasticache_egress" {
  security_group_id = aws_security_group.elasticache_sg.id
  ip_protocol       = "-1"
  cidr_ipv4         = "0.0.0.0/0"

  tags = {
    Name        = "${var.project_name}-elasticache-egress"
    Environment = var.environment
  }
}