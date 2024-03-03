
import boto3

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
    
    # Compose message
    message = f"The instance {instance_id} ({instance_type}) has {action}."
    
    # Publish message to SNS topic
    sns_client.publish(
        TopicArn=topic_arn,
        Message=message,
        Subject=f"Instance {instance_id} {action}"
    )
