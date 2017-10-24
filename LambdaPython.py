/trail-detect-unexpected-usage.pyPython

from datetime import datetime
import boto3
import json
import calendar

LOG_PERIOD     = 900 # It takes about 9 minutes to ingest log
LOG_GROUP_NAME = 'CloudTrailLogs'
TOPIC_NAME     = 'mail-iam'
SNS_SUBJECT    = 'Trail detect unexpected IAM usage'

def lambda_handler(event, context):
    logs = boto3.client('logs')
    sns  = boto3.client('sns')
    iam  = boto3.client('iam')

    #
    # Get Filter Patterns
    #
    res = logs.describe_metric_filters(
        logGroupName = LOG_GROUP_NAME,
    )['metricFilters']
    if not res: return
    filters = {x['filterName']:x['filterPattern'] for x in res}

    #
    # Get Logs
    #
    res = logs.describe_log_streams(
        logGroupName = LOG_GROUP_NAME,
        orderBy      = "LastEventTime",
        descending   = True,
        limit        = 1,
    )['logStreams']
    if not res: return

    stream_name = res[0]['logStreamName']
    end_time    = calendar.timegm(datetime.utcnow().timetuple())
    start_time  = end_time - LOG_PERIOD

    number = 0
    events = []
    for title,pattern in filters.items():
        res = logs.filter_log_events(
            logGroupName   = LOG_GROUP_NAME,
            logStreamNames = [stream_name],
            startTime      = start_time * 1000,
            filterPattern  = pattern,
        )['events']
        if not res: continue

        for event in res:
            number += 1
            event.update({'number': number, 'title': title})
            events.append(event)

    if not events:
        print "Not found filtering logs."
        return

    #
    # SNS
    #
    topics = sns.list_topics()['Topics']
    if not topics:
        print "Not found topic list."
        return
    tmp = filter(lambda x: x['TopicArn'].split(':')[-1] == TOPIC_NAME, topics)
    if not tmp:
        print "Not found topic name."
        return
    topic_arn = tmp[0]['TopicArn']

    account_alias = "NoName"
    list_account_aliases = iam.list_account_aliases()['AccountAliases']
    if list_account_aliases: account_alias = list_account_aliases[0]

    subject = "[%s] %s (%d records)" % (account_alias, SNS_SUBJECT, len(events))
    message = subject + "\n\n"
    for event in events:
        timestamp_format = datetime.fromtimestamp(event['timestamp'] / 1000)
        ingestion_format = datetime.fromtimestamp(event['ingestionTime'] / 1000)
        message += "#\n"
        message += "# %d\n" % event['number']
        message += "#\n"
        message += "Timestamp    : %s\n" % timestamp_format
        message += "ingestionTime: %s\n" % ingestion_format
        message += "Filter Name  : %s\n" % event['title']
        message += "%s\n\n" % filters[event['title']]
        message += json.dumps(json.loads(event['message']), sort_keys=True, indent=4)
        message += "\n\n"

    sns.publish(
        TopicArn = topic_arn,
        Subject  = subject,
        Message  = message,
    )
    print "Send message to SNS."
