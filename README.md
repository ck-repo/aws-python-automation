Git Repo for Automating AWS with Python, intially based on the course from A Cloud Guru but adapted with new and different features

#################################

01-Webotron:

S3 website publishing program

Webotron Features:

- Provide AWS credentials via the "--profile=<profileName>" option- 
- List S3 Buckets
- List objects in an S3 Bucket
- Creates S3 Buckets, configures Website Hosting settings and outputs S3 Endpoint URL
- Uploads HTML file to S3 and set content type to text/html
- Creates Route 53 Hosted Zones and adds "A" record to the zone that point to the alias of an S3 endpoint
- List ACM Certificates per Domain Name
- Creates CloudFront CDN that points to S3 Bucket as Origin, uses ACM SSL cert and updates R53 A Record to point to CDN

BucketManager Features:

- S3 Functions inside a class to support Webotron functionality 

DomainManager Features:

- Route53 Functions inside a class to support Webotron functionality 

CertificateManager Features:

- ACM Functions inside a class to support Webotron functionality

DistributionManager Features:

- CloudFront Functions inside a class to support Webotron functionality

Util Features:

- Host utilies to support Webotron functionality 

##################################

02-Notifon:

AWS SNS Notification program 

Notifon Features:

- Email notification of Auto Scaling Group changes using CloudWatch Events, Lambda and SNS
- Uses Serverless Framework for Infrastructure as Code deployment
