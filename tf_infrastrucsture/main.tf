terraform {
  backend "s3" {
    bucket         = "terraform.test.jpaiv.test"
    key            = "test/state/" # Format: ENVIRONMENT/state/
    region         = "eu-west-1"
    dynamodb_table = "terraform-lock"
  }
}

provider "aws" {
  region  = "eu-west-1"
  version = "3.62.0"
}

locals {
  environment_tag = "test"
}

module "vpc" {
  source            = "./modules/vpc"
  availability_zone = var.availability_zone
  vpc_cidr          = var.vpc_cidr
  subnet_cidr       = var.subnet_cidr
  environment_tag   = local.environment_tag

}

module "ec2" {
  source            = "./modules/ec2"
  availability_zone = availability_zone
  public_key_path   = var.public_key_path
  instance_ami      = var.instance_ami
  instance_type     = var.instance_type
  environment_tag   = local.environment_tag
}
