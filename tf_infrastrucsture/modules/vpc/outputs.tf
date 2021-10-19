output "vpc_id" {
  value = aws_vpc.main.id
  type  = string
}

output "subnet_id" {
  value = aws_subnet.public_subnet.id
  type  = string
}

output "security_group_id" {
  value = aws_security_group.public_port_22_security_group.id
  type  = string
}
