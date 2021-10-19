variable "environment_tag" {
  description = "Define which environment is used, normally test or prod."
  type        = string
}

variable "availability_zone" {
  description = "Give availability zone as it is, don't format it from region."
  type        = string
}

variable "subnet_cidr" {
  description = "Give availability zone as it is, don't format it from region."
  type        = string
}

variable "vpc_cidr" {
  description = "IPv 6 cidr block for VPC."
  type        = string
}
