resource "aws_route53_record" "example" {
  zone_id = var.zone_id
  name    = "${var.cluster_name}.example.com"
  type    = "A"
  ttl     = 300
  records = [var.elb_dns_name]
}
