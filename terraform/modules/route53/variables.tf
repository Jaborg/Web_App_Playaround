variable "cluster_name" {
  description = "Name of the cluster"
  type        = string
}

variable "zone_id" {
  description = "Route 53 hosted zone ID"
  type        = string
}

variable "elb_dns_name" {
  description = "DNS name of the ELB"
  type        = string
}
