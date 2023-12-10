provider "aws" {
  region = "us-east-1"  # Set your AWS region
}

# Reference the existing Lambda function
data "aws_lambda_function" "existing_lambda" {
  function_name = "test_gcp"
}

# IAM role for the Lambda function
resource "aws_iam_role" "lambda_exec_role" {
  name = "lambda_exec_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      },
    ]
  })
}

# IAM policy to allow the Lambda function to send emails via SES
resource "aws_iam_policy" "lambda_ses_policy" {
  name        = "lambda_ses_policy"
  description = "IAM policy for SES on Lambda"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = [
          "ses:SendEmail",
          "ses:SendRawEmail"
        ],
        Effect = "Allow",
        Resource = "*"
      },
    ]
  })
}

# Attach the policy to the role
resource "aws_iam_role_policy_attachment" "lambda_ses_policy_attach" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = aws_iam_policy.lambda_ses_policy.arn
}
