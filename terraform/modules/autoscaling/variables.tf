variable "cluster_name" {
  description = "Name of the cluster"
  type        = string
}

variable "min_size" {
  description = "Minimum size of the autoscaling group"
  type        = number
}

variable "max_size" {
  description = "Maximum size of the autoscaling group"
  type        = number
}
