resource "aws_autoscaling_group" "example" {
  name                      = "${var.cluster_name}-asg"
  max_size                  = var.max_size
  min_size                  = var.min_size
  desired_capacity          = var.min_size
  vpc_zone_identifier       = data.aws_subnets.default.ids
  launch_configuration      = aws_launch_configuration.example.id
  health_check_type         = "EC2"
  health_check_grace_period = 300
}

resource "aws_launch_configuration" "example" {
  name          = "${var.cluster_name}-lc"
  image_id      = "ami-12345678"
  instance_type = "t2.micro"

  lifecycle {
    create_before_destroy = true
  }
}
