resource "aws_key_pair" "ec2_public_key" {
  key_name   = "${var.environment_tag}_ec2_public_key"
  public_key = var.public_key
}

resource "aws_instance" "testInstance" {
  ami                    = var.instance_ami
  instance_type          = var.instance_type
  subnet_id              = var.subnet_id
  vpc_security_group_ids = [var.aws_security_group.id]
  key_name               = aws_key_pair.ec2_public_key.key_name
  tags {
    Environment = var.environment_tag
  }
}
