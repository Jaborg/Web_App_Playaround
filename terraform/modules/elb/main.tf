resource "aws_elb" "example" {
  name               = "${var.cluster_name}-elb"
  availability_zones = data.aws_availability_zones.available.names

  listener {
    instance_port     = local.http_port
    instance_protocol = "HTTP"
    lb_port           = local.http_port
    lb_protocol       = "HTTP"
  }

  health_check {
    target              = "HTTP:${local.http_port}/"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }
}
