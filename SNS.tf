resource "aws_sns_topic" "trail-detect-unexpected-usage" {
  name = "trail-detect-unexpected-usage"
}

resource "aws_sns_topic_subscription" "trail-detect-unexpected-usage" {
  topic_arn = "${aws_sns_topic.trail-detect-unexpected-usage.arn}"
  protocol  = "lambda"
  endpoint  = "${aws_lambda_function.trail-detect-unexpected-usage.arn}"
  endpoint_auto_confirms = false
}
