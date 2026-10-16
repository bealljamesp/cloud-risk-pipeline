output "s3_bucket_arn" {
  value       = aws_s3_bucket.risk_data.arn
  description = "ARN of the S3 portfolio bucket"
}

output "database_url" {
  value       = "postgresql+psycopg2://${var.db_password}@${aws_db_instance.postgres.address}:5432/risk_db"
  description = "PostgreSQL connection string"
  sensitive   = true
}

output "rds_endpoint" {
  value       = aws_db_instance.postgres.address
  description = "RDS PostgreSQL endpoint"
}

output "s3_bucket_name" {
  value       = aws_s3_bucket.risk_data.id
  description = "Name of the S3 bucket"
}