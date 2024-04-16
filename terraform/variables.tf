variable "server_port" {
  description = "The port the server will use for HTTP requests"
  default = 8000
}

variable "cluster_name" {
  description = "The name to use for all the cluster resources"
  type = string
  default = "Test_Jacob"
  
}

variable "min_size" {
  description = "The minimum number of EC2 Instances in the ASG"
  type = number
  default = 1
}

variable "max_size" {
  description = "The maximum number of EC2 Instances in the ASG"
  type = number
  default = 2
}

variable "AWS_ACCESS_KEY_ID" {
  description = "An example variable"
  type        = string
}

variable "AWS_SECRET_ACCESS_KEY" {
  description = "An example variable"
  type        = string
}