variable "voc_cidr" {
  description = "CIDR block for the VPC"
  default     = "10.1.0.0/16"
}

variable "subnet_cidr" {
  description = "CIDR block for the subnet"
  default     = "10.1.0.0/24"
}

variable "availability_zone" {
  description = "availability zone to create subnet"
  default     = "eu-west-1a"
}

variable "public_key" {
  description = "Public key path"
}

variable "instance_ami" {
  description = "AMI for aws EC2 instance"
  default     = "ami-0cf31d971a3ca20d6"
}

variable "instance_type" {
  description = "type for aws EC2 instance"
  default     = "t2.micro"
}
