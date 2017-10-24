resource "aws_cloudtrail" "default" {
  name = "default"

  s3_bucket_name             = "${aws_s3_bucket.log.id}"
  cloud_watch_logs_role_arn  = "${aws_iam_role.trail.arn}"
  cloud_watch_logs_group_arn = "${aws_cloudwatch_log_group.trail.arn}"

  include_global_service_events = true
  is_multi_region_trail         = true
  enable_log_file_validation    = true
}
