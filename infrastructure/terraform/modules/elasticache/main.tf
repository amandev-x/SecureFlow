# ── Subnet Group — ElastiCache needs at least 2 AZs ──────────────────────────

resource "aws_elasticache_subnet_group" "main" {
  name       = "${var.project_name}-elasticache-subnet-group"
  subnet_ids = var.private_subnet_ids

  tags = {
    Name        = "${var.project_name}-elasticache-subnet-group"
    Environment = var.environment
  }
}

# ── ElastiCache Redis Cluster ─────────────────────────────────────────────────

resource "aws_elasticache_cluster" "redis" {
  cluster_id           = "${var.project_name}-redis"
  engine               = "redis"
  engine_version       = "7.0"
  node_type            = var.redis_node_type
  num_cache_nodes      = 1
  port                 = 6379
  parameter_group_name = "default.redis7"

  subnet_group_name  = aws_elasticache_subnet_group.main.name
  security_group_ids = [var.elasticache_sg_id]

  snapshot_retention_limit = 1
  snapshot_window          = "03:00-04:00"

  maintenance_window = "mon:04:00-mon:05:00"

  apply_immediately = true

  tags = {
    Name        = "${var.project_name}-redis"
    Environment = var.environment
  }
}