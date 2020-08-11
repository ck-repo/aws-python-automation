import boto3

session = boto3.Session(profile_name='pythonAutomation')
ec2 = session.resource('ec2')
client = session.client('ec2')

key_name = 'python_automation_key'
key_path = key_name + '.pem'
key = ec2.create_key_pair(KeyName=key_name)
with open(key_path, 'w') as key_file:
    key_file.write(key.key_material) 

#permission for .pem will need to be changed to allow ssh to EC2

ami_name = 'amzn2-ami-hvm-2.0.20200722.0-x86_64-gp2'
filters = [{'Name': 'name', 'Values': [ami_name]}]
img = list(ec2.images.filter(Owners=['amazon'], Filters=filters))
for i in img:
    img = i.id

instances = ec2.create_instances(ImageId=img, MinCount=1, MaxCount=1, InstanceType='t2.micro', KeyName=key_name)

inst = instances[0]
inst.public_dns_name
inst.public_dns_name
inst.wait_until_running()
inst.reload()

inst.security_groups
client.authorize_security_group_ingress(
        GroupId= 'sg-d18fd2bb',
        IpPermissions=[
            {'IpProtocol': 'tcp',
             'FromPort': 80,
             'ToPort': 80,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp',
             'FromPort': 22,
             'ToPort': 22,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
        ])

instances.terminate()