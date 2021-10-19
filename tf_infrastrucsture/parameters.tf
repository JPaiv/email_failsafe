resource "aws_ssm_parameter" "vpc_id" {
  name        = "vpc_id"
  description = "ID of the VPC in the region"
  type        = "SecureString"
  value       = module.vpc.vpc_id
}

resource "aws_ssm_parameter" "vpc_public_subnet_id" {
  name        = "vpc_public_subnet_id"
  description = "ID of the VPC public subnetr in the region"
  type        = "SecureString"
  value       = module.vpc.subnet_id
}

resource "aws_ssm_parameter" "vpc_security_group_id" {
  name        = "vpc_security_group_id"
  description = "ID of the VPC public subnetr in the region"
  type        = "SecureString"
  value       = module.vpc.security_group_id
}

