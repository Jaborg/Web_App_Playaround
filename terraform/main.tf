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

resource "aws_launch_configuration" "example" {
  image_id        = "ami-07edc58546d708802"
  instance_type   = "t2.micro"
  security_groups = [aws_security_group.instance.id]
  key_name        = "ec2keybookreview"

  user_data = templatefile("user-data.sh", {
    AWS_ACCESS_KEY_ID     = var.AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = var.AWS_SECRET_ACCESS_KEY
  })

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
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_security_group" "elb" {
  name = "${var.cluster_name}-elb-sg"

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group_rule" "allow_elb" {
  type                     = "ingress"
  from_port                = 80
  to_port                  = 80
  protocol                 = "tcp"
  security_group_id        = aws_security_group.instance.id
  source_security_group_id = aws_security_group.elb.id
}

resource "aws_security_group_rule" "allow_elb_8000" {
  type                     = "ingress"
  from_port                = 8000
  to_port                  = 8000
  protocol                 = "tcp"
  security_group_id        = aws_security_group.instance.id
  source_security_group_id = aws_security_group.elb.id
}

resource "aws_elb" "fatdogreads" {
  name               = "fatdogreads-elb"
  availability_zones = data.aws_availability_zones.available.names
  security_groups    = [aws_security_group.elb.id]

  listener {
    instance_port     = 80
    instance_protocol = "HTTP"
    lb_port           = 80
    lb_protocol       = "HTTP"
  }

  health_check {
    target              = "HTTP:80/"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }

  tags = {
    Name = "fatdogreads-elb"
  }
}

resource "aws_autoscaling_group" "example" {
  launch_configuration = aws_launch_configuration.example.name
  vpc_zone_identifier  = data.aws_subnets.default.ids

  min_size         = 1
  max_size         = 2
  desired_capacity = 1

  health_check_type = "ELB"
  load_balancers    = [aws_elb.fatdogreads.id]

  tag {
    key                 = "Name"
    value               = "${var.cluster_name}-example"
    propagate_at_launch = true
  }

  lifecycle {
    create_before_destroy = true
  }
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

resource "aws_route53_zone" "fatdogreads" {
  name = "fatdogreads.com"
}

resource "aws_route53_record" "www_fatdogreads" {
  zone_id = aws_route53_zone.fatdogreads.zone_id
  name    = "www.fatdogreads.com"
  type    = "A"

  alias {
    name                   = aws_elb.fatdogreads.dns_name
    zone_id                = aws_elb.fatdogreads.zone_id
    evaluate_target_health = true
  }
}

resource "aws_route53_record" "root_fatdogreads" {
  zone_id = aws_route53_zone.fatdogreads.zone_id
  name    = "fatdogreads.com"
  type    = "A"

  alias {
    name                   = aws_elb.fatdogreads.dns_name
    zone_id                = aws_elb.fatdogreads.zone_id
    evaluate_target_health = true
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
