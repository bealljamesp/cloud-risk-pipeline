output "rds_endpoint" {
  value       = module.storage.rds_endpoint
  description = "PostgreSQL RDS connection endpoint"
}

output "ecs_cluster_name" {
  value       = module.compute.ecs_cluster_name
  description = "ECS Fargate Cluster Name"
}

output "s3_bucket_name" {
  value       = module.storage.s3_bucket_name
  description = "S3 bucket for portfolio ingestion"
}