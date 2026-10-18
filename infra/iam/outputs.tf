output "role_arn" {
  value = aws_iam_role.penny_get_user_budgets_function_role.arn
}

output "policy_arn" {
  value = aws_iam_policy.penny_get_user_budgets_function_policy.arn
}