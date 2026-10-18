provider "aws" {
  region = var.aws_region
}

module "lambda_iam" {
  source = "./iam"
}

resource "aws_s3_object" "lambda_package" {
  bucket = var.bucket_s3_general_state
  key    = var.lambda_s3_zip_filename
  source = "app.zip"
  etag   = filemd5("app.zip")
}

data "aws_security_group" "default" {
  id = "sg-08f6380828b2a89c5"
}

resource "aws_lambda_function" "penny_python_get_user_budgets_function" {
  function_name = var.lambda_function_name
  role          = module.lambda_iam.role_arn
  handler       = var.lambda_handler
  runtime       = var.lambda_runtime
  memory_size   = var.lambda_memory_size
  timeout       = var.lambda_timeout

  s3_bucket        = var.bucket_s3_general_state
  s3_key           = aws_s3_object.lambda_package.key
  source_code_hash = filebase64sha256("app.zip")

  vpc_config {
    subnet_ids         = var.private_subnet_ids
    security_group_ids = [data.aws_security_group.default.id]
  }
}
