resource "aws_s3_bucket" "risk_data" {
  bucket = "risk-pipeline-data-${var.environment}"
}

resource "aws_db_subnet_group" "main" {
  name       = "risk-pipeline-db-subnet-${var.environment}"
  subnet_ids = var.private_subnet_ids
}

resource "aws_db_instance" "postgres" {
  identifier             = "risk-pipeline-db-${var.environment}"
  engine                 = "postgres"
  engine_version         = "16.1"
  instance_class         = "db.t4g.micro"
  allocated_storage      = 20
  db_name                = "risk_db"
  username               = "postgres"
  password               = var.db_password
  db_subnet_group_name   = aws_db_subnet_group.main.name
  skip_final_snapshot    = true
}