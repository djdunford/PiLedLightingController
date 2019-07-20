import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    
    client = boto3.client('iot-data', region_name='eu-west-1')
    logger.info("Received event: " + json.dumps(event, indent=2))
    
    #response = client.update_thing_shadow(thingName='ThomasBedroomLEDcontrol')
    
    
    
    #streamingBody = response["payload"]
    #jsonState = json.loads(streamingBody.read())
    #logger.info(jsonState)
 
    #return {'statusCode': 200, 'body': json.dumps(jsonState), 'headers': {'Content-Type': 'application/json'}}
    return {'statusCode': 200}
