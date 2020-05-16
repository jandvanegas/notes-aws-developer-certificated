# Chapter 1: Introduction to AWS Cloud API
![](image.png)

Options for managing AWS resources

*  Install boto3 (AWS SDK for python)
	* `pip install boto3 --upgrade -use`

## Api Example: Hello World
The code request to Amazon Polly (It provides test-to-speech service with natural-sounding speech)

```

import boto3
import configparser
import os
config = configparser.ConfigParser()
path = os.path.join(os.path.expanduser('~'), '.aws/credentials')
config.read(path)
aws = config['default']

polly = boto3.client('polly',
	region_name='us-east-1',
	aws_access_key_id=aws['aws_access_key_id'],
	aws_secret_access_key=aws['aws_secret_access_key'],
	)

result = polly.synthesize_speech(Text='Nia, Juan Andres loves you',
	OutputFormat='mp3',
	VoiceId='Aditi')

audio = result['AudioStream'].read()
with open("helloworld.mp3", "wb") as file:
	file.write(audio)

```

This is the process which the script follows
![](image_1.png)

API Requests
```
POST /v1/speech HTTP/1.1 host: polly.us-west-2.amazonaws.com
content-Type: application/json
x-amz-date: 20180411T051402Z
authorization: AWS4-HMAC-SHA256 Credential=AKIAIO5FODNN7EXAMPLE/20180411/us-west-2/polly/aws4_request, SignedHeaders=content-length;content-type;host;x-amz-date, Signature=d968197e88a6a8de69d1a7bcab414669eecd5f841e13dc90e4a7852c2c428038
 
{
       "OutputFormat": "mp3",
       "Text" : "Hello World!",
       "VoiceId": "Aditi"
}
```

API Response

```
HTTP/1.1 200
status: 200
content-type: audio/mpeg
date: Wed, 11 Apr 2018 05:14:02 GMT
x-amzn-requestcharacters: 12
x-amzn-requestid: 924141bb-b0a6-11e8-b565-b1fabccdcbd9
transfer-encoding: chunked
connection: keep-alive
```

Install CLI
* [link](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
There are two version. The first one requiers python packages. The second is install in bin folder

Configure credentials `aws configure`
https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html

## Working with Regional API Endpoints
* Ussually the endpoint contains the region
![](image_2.png)

## Identifying AWS Regions

![](image_3.png)
* The Api endpoint for IAM is the same ragardless of the region
* [Information about all of the APIs](https://docs.aws.amazon.com/general/latest/gr/rande.html)

![](image_4.png)

## API Credentials and AWS Identity and Access Management
* To manage authentication and authorization for people or applications , IAM proveides users, groups and roles as identities that you can manage.
* IAM authenticates the security credentials used to sign and API call to verify that the request is coming from and a known identity. Then, IAM authorizes the rquest by evaluating the policies associated with the identity and resources affected by the reques.
* When you first created an account and sign in with wour email address and password you are authenticating as the root user permissions.
* Do not generate an access key based on the roor user.
* Create an IAM user and generate an access key.

### Users

![](image_5.png)

### AWS IAM User API Access Keys
For programmatic access, create an access key for teh IAM user.
It is composed of 
* Access Key ID
* Secret access key
Each user may have up to two active acess keys at any time.

In addition to theses authentication. You can have X.509 certificatees (Soap APIs), git credentials.

### Groups
* They do not have theri own credentials.
* When a user makes an API call, AWS looks up that user's groups memberships and finds the relevant perissions policies
* Associate user with a group and assing plicies to the group insteadof associatin the permissions directly to each user
* User group has a relationship many to many.

![](image6.png)

* In case that multiple permissions policies apply to the same API action, any policy that  has the effect deny will take precedence over any policy that has the effect allow.

### Roles 
* For not long-term credentials

![](image7.png)

* Define a trsut policy that specifieswhich principals can assume a role
* protential principals include:
	* AWS services
	* Users who have authenticated using identity federation

Example of trust policy

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com"

      },
      "Action": "sts:AssumeRole"

    }
  ]
}

```

* AWS providesnew short-term security credentials that are valid for a time-limited session through AWS Security Token Service (STS)
* These credentials are composed of 
	* access key ID
	* secred access key
	* session token with a know expiration date

Like this

```
{
       "AccessKeyId": "ASIAJHP2KG65VIKQU2XQ",
       "SecretAccessKey": "zkvPEbYxCLVVD0seWdRnesc8krNDPHEX1cFMyI5W",
       "SessionToken":
"FQoDYXdzEMf//////////wEaDL1b0Wd7VTA3J25cNyL4ARzNSRczH4U3f8gJwi1W8XiDLWJIE9EdX
4l4KXTiST40gPoWc9Do9QkcN2xRHk6/qVT6W23d0u6+5YFY9C2wnoEeTTmiQBT5SMjqku5MYlhrCDy
FQAVbo6RKUeOZXXSG8REshuFGBtaCNmv95lFF6srCT1b4FZtTtULE7WV3LMcDs6Z2XuN+6aGTawhY5
0RMnlKRL1w6yHq++RysQWbBHkuNeK/VqjueDINFODPOje9ZnYePVjR5uLmL8ZARWYVBFrB2tpxG07/
dseUS9O2q1hMP8DJuEfsbaiK2ASsmXSRA8vOZnuu4AsBq6ERasBw5EcpICP/Ne8zdKO/93tYF",
        "Expiration": "2018-04-18T22:55:59Z"
}
```
* AWS looks up the permissions policies associated with the IAM role, not others, even if the principal was an user.
* You cannot next IAM roles or add IAM orles to IAM grops

![](image8.png)

### Choosing IAM identities

![](image9.png)

### Managing authorization with policies

* Any API is implicitly denied unless there is a policy that explicitly allows it.
* If there is a policy that explicityly denies an action, that policy always takes precedence.
* AWS recommends that you adopt the principle of least privilege.
* One method of granting perissions is to use AWS managed policies.
* Managed policies supposrt common tasks and are automatically updated as new services and API operations are added.

Example: AmazonPollyReadOnlyAccess policy is defined as
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "polly:DescribeVoices",
                "polly:GetLexicon",
                "polly:ListLexicons",
                "polly:SynthesizeSpeech"
            ],
            "Resource": [
                "*"
            ]
        }
    ]
}
```


### Custom policies
* AWS recommends that you use the AWS manged policies whenever possible. However, when you need more control you candefine custom policies

* An IAM policy is a JSON-style document compsed of:
	* One or more statements
		* Effect: allow or deny access
		* Action: actions on AWS resources
		* Resource: specific ARN (Amazon Resource Name) or wildcards
		* Sid: statement id for additional components
		* Condition Block
		* Principal: if the policy is attached to a resource

![](image_10.png)

Example

```
{
  "Version": "2012-10-17",
  "Statement": [{
      "Sid": "AllowDeleteSpecifiedRegion",
      "Effect": "Allow",
      "Action": [
         "polly:DeleteLexicon"],
      "Resource": "arn:aws:polly:us-east-2:123456789012:lexicon/*"
      }
   ]
}
```
Wildcards for ARN. An ARN start with arn: and can include

* Partition: usually aws, for some regions as in China this can change
* Service: namespace. e.g. polly
* Region
* Accound ID
* Resource

Example

```
arn:partition:service:region:account-id:resource
arn:partition:service:region:account-id:resourcetype/resource
arn:partition:service:region:account-id:resourcetype:resource

<!-- Amazon Polly Lexicon -->
arn:aws:polly:us-west-2:123456789012:lexicon/awsLexicon
 
<!-- IAM user name -->
arn:aws:iam::123456789012:user/carla
 
 
<!-- Object in an Amazon S3 bucket -->
arn:aws:s3:::bucket-name/exampleobject.png
```

### Useful commands
* `aws configure get region`

