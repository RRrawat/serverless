import boto3
import os
import logging
import logging as log
import yaml
import json 

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_env_var(env_var):
    return os.getenv(env_var, None)

email_address = get_env_var('EMAIL_ADDRESSES')
email_addresses = [email.strip() for email in email_address.split(',')]

def create_sns_topics_and_subscriptions(topic_names):
    sns_client = boto3.client('sns')
    topic_arns = []

    for topic_name in topic_names:
        # Check if topic already exists
        response = sns_client.list_topics()
        existing_topics = [topic['TopicArn'] for topic in response.get('Topics', [])]
        topic_arn = next((arn for arn in existing_topics if arn.endswith(':' + topic_name)), None)

        if topic_arn:
            # Topic already exists, append its ARN to the list
            topic_arns.append(topic_arn)
            logger.info("SNS Topic %s already exists.", topic_name)
        else:
            response = sns_client.create_topic(Name=topic_name)
            topic_arn = response['TopicArn']
            topic_arns.append(topic_arn)

            policy_document = {
                "Id": "CloudWatchAlarmPermission",
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "CloudWatchAlarmTrigger",
                        "Effect": "Allow",
                        "Principal": {
                            "Service": "cloudwatch.amazonaws.com"
                        },
                        "Action": "sns:Publish",
                        "Resource": topic_arn
                    }
                ]
            }

            # Create the SNS topic policy
            sns_client.set_topic_attributes(
                TopicArn=topic_arn,
                AttributeName="Policy",
                AttributeValue=json.dumps(policy_document)
            )
            logger.info("SNS Topic Policy has been created and associated with the SNS topic.")
            
            # Create an SNS subscription for email notifications for the new topic
            for email_address in email_addresses:
                subscription = sns_client.subscribe(
                    TopicArn=topic_arn,
                    Protocol="email",
                    Endpoint=email_address
                )
                logger.info(subscription)
                logger.info("SNS Topic %s", topic_name)

    logger.info("topic_arns: %s", topic_arns)
    return topic_arns