import boto3
import logging as log
from common import create_sns_topics_and_subscriptions, get_env_var, get_config_value, alarm_exists,generate_alarm_name


log.basicConfig(level=log.INFO, format='%(asctime)s %(levelname)s %(message)s')
log.getLogger('boto3').setLevel(log.ERROR)
log.getLogger('botocore').setLevel(log.ERROR)

period = get_config_value('Period', 'EC2')
evaluation_periods = get_config_value('FreeStorageThreshold', 'EC2')
threshold = get_config_value('Threshold', 'EC2')
baseStackName = get_env_var('STACKBASE_NAME')
    
def create_cloudwatch_alarm(sns_topic_arns, baseStackName, instance_id):
    cloudwatch = boto3.client('cloudwatch')
    try:
        for sns_topic_arn in sns_topic_arns:
            log.info("topic_arn: %s", sns_topic_arn)
            suffix = (f"CWEC2-{instance_id}")
            alarm_name = generate_alarm_name(baseStackName, sns_topic_arn, suffix)
            alarm_actions = [sns_topic_arn]

            # Check if the alarm already exists
            if alarm_exists(cloudwatch, alarm_name):
                log.info(f"Alarm {alarm_name} already exists. Skipping creation.")
                continue
            
            if 'CPUUtilization' in sns_topic_arn:
                cloudwatch.put_metric_alarm(
                    AlarmName=alarm_name,
                    AlarmDescription='High CPU Utilization Alarm',
                    ActionsEnabled=True,
                    AlarmActions=alarm_actions,
                    MetricName='CPUUtilization',
                    Namespace='AWS/EC2',
                    Statistic='Average',
                    Dimensions=[
                        {
                            'Name': 'InstanceId',
                            'Value': instance_id
                        },
                    ],
                    Period=int(period),
                    EvaluationPeriods=int(evaluation_periods),
                    Threshold=int(threshold),
                    ComparisonOperator='GreaterThanThreshold',
                    TreatMissingData='notBreaching'
                )
            
            # Create CloudWatch alarms for StatusCheckFailed based on topic ARN
            if 'StatusCheckFailed' in sns_topic_arn:
                cloudwatch.put_metric_alarm(
                    AlarmName=alarm_name,
                    AlarmDescription='Status Check Failed Alarm',
                    ActionsEnabled=True,
                    AlarmActions=alarm_actions,
                    MetricName='StatusCheckFailed',
                    Namespace='AWS/EC2',
                    Statistic='Maximum',
                    Dimensions=[
                        {
                            'Name': 'InstanceId',
                            'Value': instance_id
                        },
                    ],
                    Period=300,  # 5 minutes
                    EvaluationPeriods=3,
                    Threshold=0.0,
                    ComparisonOperator='GreaterThanThreshold',
                    TreatMissingData='notBreaching'
                )

            log.info("CloudWatch alarms created successfully.")
    except Exception as e:
        log.error(f"Error: {str(e)}")

def delete_cloudwatch_alarms(sns_topic_arns, instance_id):
    cw_client = boto3.client('cloudwatch')
    try:
        for sns_topic_arn in sns_topic_arns:
            suffix = (f"CWEC2-{instance_id}")
            alarm_name = generate_alarm_name(baseStackName, sns_topic_arn, suffix)
            # Delete CloudWatch Alarms
            cw_client.delete_alarms(AlarmNames=[alarm_name])
            log.info(f'CloudWatch alarm deleted: {alarm_name}')
    except Exception as e:
        log.error(f"Error: {str(e)}")

def handler(event, context):
    try:
        global baseStackName

        # Setting up default topic names as per requirements
        topic_names = [f'{baseStackName}-CPUUtilization-SNSTopic', f'{baseStackName}-StatusCheckFailed-SNSTopic']
        # Retrieve SNS ARNs using the common function
        sns_topic_arn = create_sns_topics_and_subscriptions(topic_names)
        
        if 'detail' in event:
            if event['detail']['state'] == 'running':
                instance_id = event['detail']['instance-id']
                create_cloudwatch_alarm(sns_topic_arn, baseStackName, instance_id)
            elif event['detail']['state'] == 'terminated':
                instance_id = event['detail']['instance-id']
                delete_cloudwatch_alarms(sns_topic_arn, instance_id)
        #TO DO
        elif 'details' in event:
            for instance_id in event['detail']['instance-ids']:
                if event['details']['action'] == 'create':
                    create_cloudwatch_alarm(sns_topic_arn, baseStackName, instance_id)
                else:
                    delete_cloudwatch_alarms(sns_topic_arn, instance_id)
    except Exception as e:
        log.error("An error occurred: {}".format(e))