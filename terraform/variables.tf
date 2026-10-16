variable "aws_region" {
  type        = string
  default     = "us-west-2"
  description = "Target AWS Region"
}

variable "environment" {
  type        = string
  default     = "production"
  description = "Deployment environment name"
}

variable "db_password" {
  type        = string
  sensitive   = true
  description = "PostgreSQL master password"
}