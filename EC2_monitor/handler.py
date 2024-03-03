
import boto3
from cwalarms import create_cloudwatch_alarm, delete_cloudwatch_alarms
from snstopic import create_sns_topics_and_subscriptions

def lambda_handler(event, context):
    # Create an SNS client
    sns_client = boto3.client('sns')
    
    # Create an SNS topic
    response = sns_client.create_topic(Name='InstanceEventsTopic')
    topic_arn = response['TopicArn']
    
    # Extract instance event details from the event
    instance_id = event['detail']['instance-id']
    state = event['detail']['state']
    instance_type = event['detail']['instance-type']
    
    # Determine the action
    action = "started" if state == "running" else "terminated"
    # Setting up default topic names as per requirements
    topic_names = [f'demo-EC2-Monitor-SNSTopic']
        # Retrieve SNS ARNs using the common function
    sns_topic_arn = create_sns_topics_and_subscriptions(topic_names)
    if 'detail' in event:
            if event['detail']['state'] == 'running':
                instance_id = event['detail']['instance-id']
                create_cloudwatch_alarm(sns_topic_arn, instance_id)
                # Compose message
                message = f"The instance {instance_id} ({instance_type}) has {action}."
            elif event['detail']['state'] == 'terminated':
                instance_id = event['detail']['instance-id']
                delete_cloudwatch_alarms()
                # Compose message
                message = f"The instance {instance_id} ({instance_type}) has {action}."
    sns_client.publish(
        TopicArn=sns_topic_arn,
        Message=message,
        Subject=f"Instance {instance_id} {action}"
    )
