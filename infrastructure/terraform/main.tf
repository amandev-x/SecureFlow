# ── VPC ───────────────────────────────────────────────────────────────────────
module "vpc" {
  source = "./modules/vpc"

  project_name         = var.project_name
  environment          = var.environment
  vpc_cidr             = "10.0.0.0/16"
  public_subnet_cidrs  = ["10.0.1.0/24", "10.0.2.0/24"]
  private_subnet_cidrs = ["10.0.3.0/24", "10.0.4.0/24"]
  availability_zones   = ["ap-south-1a", "ap-south-1b"]
}

# ── Security Groups ───────────────────────────────────────────────────────────
module "security-groups" {
  source = "./modules/security-groups"

  project_name = var.project_name
  environment  = var.environment
  vpc_id       = module.vpc.vpc_id
  my_ip        = var.my_ip
}

# ── EC2 ───────────────────────────────────────────────────────────────────────
module "ec2" {
  source = "./modules/ec2"

  project_name          = var.project_name
  environment           = var.environment
  app_instance_type     = "m7i-flex.large"
  jenkins_instance_type = "t3.small"
  public_subnet_id      = module.vpc.public_subnet_ids[0]
  app_server_sg_id      = module.security-groups.app_server_sg_id
  jenkins_sg_id         = module.security-groups.jenkins_sg_id
  key_name              = var.key_pair_name
}

# ── RDS ───────────────────────────────────────────────────────────────────────
module "rds" {
  source = "./modules/rds"

  project_name       = var.project_name
  environment        = var.environment
  private_subnet_ids = module.vpc.private_subnet_ids
  rds_sg_id          = module.security-groups.rds_sg_id
  db_instance_class  = "db.t4g.micro"
  db_username        = "postgres"
  db_password        = var.db_password
}

# ── ElastiCache ───────────────────────────────────────────────────────────────
module "elasticache" {
  source = "./modules/elasticache"

  project_name       = var.project_name
  environment        = var.environment
  private_subnet_ids = module.vpc.private_subnet_ids
  elasticache_sg_id  = module.security-groups.elasticache_sg_id
  redis_node_type    = "cache.t3.micro"
}

# ── ECR ───────────────────────────────────────────────────────────────────────
module "ecr" {
  source = "./modules/ecr"

  project_name = var.project_name
  environment  = var.environment

  service_names = [
    "api-gateway",
    "user-service",
    "product-service",
    "order-service",
    "notification-service"
  ]
}