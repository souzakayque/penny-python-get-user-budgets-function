output "lambda_arn" {
  value       = aws_lambda_function.penny_python_get_user_budgets_function.arn
  description = "ARN da função Lambda"
}
