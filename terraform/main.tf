provider "aws" {
  region = "eu-west-1" # Change this to your desired region
}


locals {
  http_port = 8000
  any_port = 0
  any_protocol = "-1"
  tcp_protocol = "tcp"
  all_ips = ["0.0.0.0/0"]
}



resource "aws_launch_configuration" "example" {
  image_id        = "ami-07edc58546d708802"
  instance_type   = "t2.small"
  security_groups = [aws_security_group.instance.id]
  key_name      = "ec2keybookreview"

  user_data = templatefile("user-data.sh", {
    AWS_ACCESS_KEY_ID = var.AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY  = var.AWS_SECRET_ACCESS_KEY
  })


  # Required when using a launch configuration with an auto scaling group.
  lifecycle {
    create_before_destroy = true
  }
}


resource "aws_security_group" "instance" {

  name = "${var.cluster_name}-instance"

  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Allow SSH from any IP. You can restrict it to specific IPs if needed.
  }

    # Egress rules
  egress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    cidr_blocks     = ["0.0.0.0/0"]  # Allow outbound traffic to all IP addresses
  }

  egress {
    from_port       = 80
    to_port         = 80
    protocol        = "tcp"
    cidr_blocks     = ["0.0.0.0/0"]  # Allow outbound HTTP traffic
  }

  egress {
    from_port       = 443
    to_port         = 443
    protocol        = "tcp"
    cidr_blocks     = ["0.0.0.0/0"]  # Allow outbound HTTPS traffic
  }
  lifecycle{
  create_before_destroy = true
 }
}


resource "aws_autoscaling_group" "example"{
  launch_configuration = aws_launch_configuration.example.name
  vpc_zone_identifier = data.aws_subnets.default.ids


  min_size = 1
  max_size = 2

  tag {
    key = "Name"
    value = "${var.cluster_name}-example"
    propagate_at_launch = true
  }
}

data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

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
}