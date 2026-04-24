# ── App Server IAM Role (pull only) ──────────────────────────────────────────

resource "aws_iam_role" "app_server_role" {
  name = "${var.project_name}-app-server-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name        = "${var.project_name}-app-server-role"
    Environment = var.environment
  }
}

# ── Jenkins IAM Role (pull + push) ───────────────────────────────────────────
resource "aws_iam_role" "jenkins_role" {
  name = "${var.project_name}-jenkins-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name        = "${var.project_name}-jenkins-role"
    Environment = var.environment
  }
}