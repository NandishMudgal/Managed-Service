import boto3

iam = boto3.client('iam')
sns = boto3.client('sns')

topic = "arn:aws:sns:us-east-1:411815166437:thenmozhy-topic"

Telos_buckets = ['xacta-audit-stage', 'xacta-cloudtraillogs-stage', 'xacta-messages-stage', 'xacta-stage-build-pipeline-artifacts', 'xacta-stage-customer-artifacts', 'xacta-stage-releases']
               
def lambda_handler(event, context):
    try:

        bucket = event['detail']['requestParameters']['bucketName']
        action = event['detail']['eventName']
        crossrole = event['detail']['userIdentity']['sessionContext']

        if bucket in Telos_bucket:        
            if 'sessionIssuer' in crossrole:
                arn = crossrole['sessionIssuer']['arn'].split("/")
                role = iam.get_role(RoleName=arn[1])
                principle = role['Role']['AssumeRolePolicyDocument']['Statement']
                Id = ""
                for acc in principle:
                    crossAccount = acc['Principal']['AWS'].split("::")
                    accountId = crossAccount[1].split(":")
                    Id += accountId[0]

                message = "BucketName: "+ bucket + "\nAction Performed: " + action + "\nFrom the account: " + Id                            
                response = sns.publish(
                    TopicArn=topic,
                    Message= message,
                    Subject='Buckets accessed by cross account'
                )
                
                print "The bucket " + bucket + " is accessed by cross account"
            
            else:
                print "The bucket " + bucket + " is not accessed by cross account"
        else:
            print "The bucket is not monitored by Telos"
           
    except Exception as e:
            print (str(e))