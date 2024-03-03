import boto3
import logging as log

log.basicConfig(level=log.INFO, format='%(asctime)s %(levelname)s %(message)s')
log.getLogger('boto3').setLevel(log.ERROR)
log.getLogger('botocore').setLevel(log.ERROR)

def create_cloudwatch_alarm(sns_topic_arns, instance_id):
    cloudwatch = boto3.client('cloudwatch')
    try:
        for sns_topic_arn in sns_topic_arns:
            log.info("topic_arn: %s", sns_topic_arn)
            alarm_actions = [sns_topic_arn]
            
            cloudwatch.put_metric_alarm(
                AlarmName='demo-EC2-CPU-Utilization-Alarm',
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
                Period=300,
                EvaluationPeriods=6,
                Threshold=95,
                ComparisonOperator='GreaterThanThreshold',
                TreatMissingData='notBreaching'
            )
        
        # Create CloudWatch alarms for StatusCheckFailed based on topic ARN
        
            cloudwatch.put_metric_alarm(
                AlarmName='demo-EC2-Status-Check-Failed-Alarm',
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

def delete_cloudwatch_alarms():
    cw_client = boto3.client('cloudwatch')
    try:
        alarm_names = ['demo-EC2-CPU-Utilization-Alarm', 'demo-EC2-Status-Check-Failed-Alarm']
        # Delete CloudWatch Alarms
        for alarm_name in alarm_names:
            cw_client.delete_alarms(AlarmNames=[alarm_name])
            log.info(f'CloudWatch alarm deleted: {alarm_name}')
    except Exception as e:
        log.error(f"Error: {str(e)}")
