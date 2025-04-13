provider "aws" {
  region = "eu-west-1"
}

locals {
  http_port    = 8000
  any_port     = 0
  any_protocol = "-1"
  tcp_protocol = "tcp"
  all_ips      = ["0.0.0.0/0"]
}

module "security_groups" {
  source       = "./modules/security_groups"
  cluster_name = var.cluster_name
}

module "elb" {
  source       = "./modules/elb"
  cluster_name = var.cluster_name
}

module "autoscaling" {
  source                = "./modules/autoscaling"
  cluster_name          = var.cluster_name
  AWS_ACCESS_KEY_ID     = var.AWS_ACCESS_KEY_ID
  AWS_SECRET_ACCESS_KEY = var.AWS_SECRET_ACCESS_KEY
}

module "route53" {
  source       = "./modules/route53"
  cluster_name = var.cluster_name
}

data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

data "aws_availability_zones" "available" {}

output "ACCESS_KEY" {
  value = var.AWS_ACCESS_KEY_ID
}

output "SECRET_KEY" {
  value = var.AWS_SECRET_ACCESS_KEY
}

output "rendered_user_data" {
  value = templatefile("user-data.sh", {
    AWS_ACCESS_KEY_ID     = var.AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = var.AWS_SECRET_ACCESS_KEY
  })
  sensitive = true
}
