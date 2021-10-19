resource "aws_vpc" "main" {
  cidr_block       = var.vpc_cidr
  instance_tenancy = "default"

  tags = {
    Environment = var.environment_tag
  }
}

resource "aws_internet_gateway" "internet_gateway" {
  vpc_id = aws_vpc.main.id

  tags {
    Environment = var.environment_tag
  }
}

resource "aws_subnet" "public_subnet" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.subnet_cidr
  map_public_ip_on_launch = "true"
  availability_zone       = var.availability_zone
  tags {
    Environment = var.environment_tag
  }
}

resource "aws_route_table" "public_route_table" {
  vpc_id = aws_vpc.vpc.id
  route {
    cidr_block = "0.0.0.0/0" # Allow all
    gateway_id = aws_internet_gateway.internet_gateway.id
  }
  tags {
    Environment = var.environment_tag
  }
}

resource "aws_route_table_association" "public_route_table_subnet_association" {
  subnet_id      = aws_subnet.subnet_public.id
  route_table_id = aws_route_table.public_route_table.id
  tags {
    Environment = var.environment_tag
  }
}

resource "aws_security_group" "public_port_22_security_group" {
  name   = "${var.environment_tag}_public_port_22_security_group"
  vpc_id = aws_vpc.main.id
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags {
    Environment = var.environment_tag
  }
}