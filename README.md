Git Repo for Automating AWS with Python, intially based on the course from A Cloud Guru

#######

01-Webotron:

S3 website publishing program

Webotron Features:

- List S3 Buckets
- List objects in an S3 Bucket
- Create an S3 Bucket ready for Website Hosting and output S3 Endpoint URL
- Upload file to S3 and set content type to text/html
- Provide AWS credentials via the "--profile=<profileName>" option
- Setup Route 53 Hosted Zones and add "A" records to the zone that point to the alias of an S3 website
- List ACM Certificates per Domain Name

BucketManager Features:

- S3 Functions inside a class to support Webotron functionality 

DomainManager Features:

- Route53 Functions inside a class to support Webotron functionality 

CertificateManager Features:

- ACM Functions inside a class to support Webotron functionality

Util Features:

- Host utilies to support Webotron functionality 