variable "environment" { type = string }
variable "vpc_id" { type = string }
variable "private_subnet_ids" { type = list(string) }
variable "s3_bucket_arn" { type = string }
variable "database_url" { type = string }