resource "aws_cloudwatch_log_group" "trail" {
  name = "CloudTrailLogs"
  retention_in_days = 3
}

resource "aws_cloudwatch_log_metric_filter" "trail-console-login-outside-of-office" {
  name = "TrailConsoleLoginOutsideOfOffice"
  pattern = <<PATTERN
    { $.responseElements.ConsoleLogin = "Success" && $.sourceIPAddress != "1.2.3.*" }
PATTERN
  log_group_name = "${aws_cloudwatch_log_group.trail.name}"

  metric_transformation {
    name = "TrailConsoleLoginOutsideOfOffice"
    namespace = "LogMetrics"
    value = "1"
  }
}

resource "aws_cloudwatch_log_metric_filter" "trail-console-login-failure" {
  name = "TrailConsoleLoginFailure"
  pattern = <<PATTERN
    { $.responseElements.ConsoleLogin = "Failure" }
PATTERN
  log_group_name = "${aws_cloudwatch_log_group.trail.name}"

  metric_transformation {
    name = "TrailConsoleLoginFailure"
    namespace = "LogMetrics"
    value = "1"
  }
}
