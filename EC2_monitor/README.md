# EC2 Monitoring Application

This application provides real-time monitoring for EC2 instances, notifying users about instance state changes and setting up CloudWatch alarms for critical metrics.

## Functionality

- **Instance State Change Notifications**: The application triggers notifications whenever an EC2 instance is created or terminated, providing users with timely updates on instance lifecycle events.

- **CloudWatch Alarms**: It automatically sets up CloudWatch alarms for CPU utilization and status check failures upon instance creation. These alarms help in proactive monitoring and alerting, ensuring timely action in case of performance issues or instance health concerns.

## Deployment Steps

1. **Clone the Repository**: Clone the repository to your local machine.

    ```bash
    git clone <repository_url>
    ```

2. **Install Serverless Framework**: Install the Serverless Framework globally using npm.

    ```bash
    npm install -g serverless
    ```

3. **Configure AWS CLI**: Ensure that your AWS CLI is configured with the necessary credentials to deploy resources to AWS.

    ```bash
    aws configure
    ```

4. **Deploy the Application**: Use the Serverless Framework to deploy the application to your AWS account.

    ```bash
    serverless deploy
    ```

5. **Verify Deployment**: Once the deployment is complete, verify that the application is working as expected by monitoring EC2 instance state changes and CloudWatch alarms in the AWS Management Console.

## Additional Notes

- **Permissions**: Ensure that the IAM role used for deployment has sufficient permissions to create CloudWatch alarms, publish SNS notifications, and access EC2 instance information.

- **GitHub Integration**: To receive notifications in a GitHub repository, configure the appropriate webhook or integration settings to receive updates from the SNS topic created by the application.

- **Monitoring Strategy**: Customize CloudWatch alarm thresholds and monitoring strategies based on your specific requirements and performance metrics.

By following these deployment steps, you can set up an effective monitoring system for EC2 instances, enhancing visibility and facilitating proactive management of your AWS resources.

For further details, please contact mailtorahulrawat1097@gmail.com.
