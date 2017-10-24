resource "aws_s3_bucket" "log" {
  bucket = "${var.company_name}-${var.service_name}-log"

  lifecycle_rule {
      id = "log"
      prefix = "AWSLogs/"
      enabled = true

      transition {
          days = 30
          storage_class = "GLACIER"
      }
      expiration {
          days = 365
      }
  }

  policy = <<POLICY
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AWSCloudTrailAclCheck",
            "Effect": "Allow",
            "Principal": {
               "Service": "cloudtrail.amazonaws.com"
            },
            "Action": "s3:GetBucketAcl",
            "Resource": "arn:aws:s3:::${var.company_name}-${var.service_name}-log"
        },
        {
            "Sid": "AWSCloudTrailWrite",
            "Effect": "Allow",
            "Principal": {
               "Service": "cloudtrail.amazonaws.com"
            },
            "Action": "s3:PutObject",
            "Resource": "arn:aws:s3:::${var.company_name}-${var.service_name}-log/AWSLogs/*",
            "Condition": {
                "StringEquals": {
                    "s3:x-amz-acl": "bucket-owner-full-control"
                }
            }
        }
    ]
}
POLICY
}
