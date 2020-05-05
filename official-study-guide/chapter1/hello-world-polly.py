import boto3
import configparser
import os
import logging
logging.basicConfig(
        level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(message)s'
    )
logger = logging.getLogger()
logger.debug('The script is starting.')
logger.info('Connecting to EC2...')
boto3.set_stream_logger('', logging.DEBUG)
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

