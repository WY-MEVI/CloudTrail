resource "aws_cloudwatch_metric_alarm" "trail-console-login-outside-of-office" {
    alarm_name  = "${aws_cloudwatch_log_metric_filter.trail-console-login-outside-of-office.name}"
    metric_name = "${aws_cloudwatch_log_metric_filter.trail-console-login-outside-of-office.name}"
    namespace   = "LogMetrics"

    comparison_operator = "GreaterThanOrEqualToThreshold"
    evaluation_periods  = "1"

    period    = "300"
    statistic = "Sum"
    threshold = "1"
    alarm_description = "Trail detect console login outside of office"
    alarm_actions = ["${aws_sns_topic.trail-detect-unexpected-usage.arn}"]
}

resource "aws_cloudwatch_metric_alarm" "trail-console-login-failure" {
    alarm_name  = "${aws_cloudwatch_log_metric_filter.trail-console-login-failure.name}"
    metric_name = "${aws_cloudwatch_log_metric_filter.trail-console-login-failure.name}"
    namespace   = "LogMetrics"

    comparison_operator = "GreaterThanOrEqualToThreshold"
    evaluation_periods  = "1"

    period    = "300"
    statistic = "Sum"
    threshold = "1"
    alarm_description = "Trail detect console login failure"
    alarm_actions = ["${aws_sns_topic.trail-detect-unexpected-usage.arn}"]
}
