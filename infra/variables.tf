variable "aws_region" {
  description = "Região AWS onde os recursos serão criados"
  type        = string
  default     = "us-east-2"
}

variable "lambda_function_name" {
  description = "Nome da função Lambda"
  type        = string
  default     = "penny-python-get-user-budgets-function"
}

variable "lambda_runtime" {
  description = "Ambiente de execução da Lambda"
  type        = string
  default     = "python3.12"
}

variable "lambda_handler" {
  description = "Handler da função Lambda"
  type        = string
  default     = "app.lambda_handler"
}

variable "lambda_memory_size" {
  description = "Tamanho da memória para a função Lambda (MB)"
  type        = number
  default     = 128
}

variable "lambda_timeout" {
  description = "Timeout da função Lambda (em segundos)"
  type        = number
  default     = 30
}

variable "lambda_s3_zip_filename" {
  description = "Nome do arquivo terraform no S3"
  type        = string
  default     = "penny_python_get_user_budgets_lambda.zip"
}


variable "bucket_s3_general_state" {
  description = "Nome do Bucket S3 para publicacoes terraform"
  type        = string
  default     = "penny-infra-s3-general-state"
}

variable "private_subnet_ids" {
  description = "Lista de subnets privadas"
  type = list(string)
  default = ["subnet-01320cca0220aae1e"]
}

variable "vpc_id" {
  description = "ID da VPC onde a Lambda será implantada"
  type        = string
  default     = "vpc-01c36bf14c79fa78f"
}