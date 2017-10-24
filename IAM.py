resource "aws_iam_role" "lambda_vpc" {
  name = "lambda_basic_vpc_execution"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "lambda_vpc" {
  name = "lambda_basic_vpc_execution_policy"
  role = "${aws_iam_role.lambda_vpc.id}"
  policy = <<EOT
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "ec2:CreateNetworkInterface",
                "ec2:DescribeNetworkInterfaces",
                "ec2:DetachNetworkInterface",
                "ec2:DeleteNetworkInterface"
            ],
            "Resource": "*"
        },
        {
          "Effect": "Allow",
          "Action": [
            "lambda:*",
            "iam:List*",
            "sns:Publish",
            "sns:List*",
            "logs:Get*",
            "logs:Describe*",
            "logs:Filter*"
          ],
          "Resource": "*"
        },
        {
          "Effect": "Allow",
          "Action": [
            "cloudwatch:ListMetrics",
            "cloudwatch:GetMetricStatistics",
            "cloudwatch:Describe*"
          ],
          "Resource": "*"
        }
    ]
}
EOT
}
