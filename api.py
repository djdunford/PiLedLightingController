import json
import boto3
import logging

logger = logging.getLogger("api")
logger.setLevel(logging.INFO)
iotClient = boto3.client('iot-data', region_name='eu-west-1')

def showsequence(event, context):
    
    logger.info("Received event: " + json.dumps(event, indent=2))
    logger.info("sequence: " + event['pathParameters']['sequence'])
    
    #response = client.update_thing_shadow(thingName='ThomasBedroomLEDcontrol')
    
    
    
    #streamingBody = response["payload"]
    #jsonState = json.loads(streamingBody.read())
    #logger.info(jsonState)
 
    #return {'statusCode': 200, 'body': json.dumps(jsonState), 'headers': {'Content-Type': 'application/json'}}
    return {'statusCode': 200}

def state(event, context):
	response = iotClient.get_thing_shadow(thingName='ThomasBedroomLEDcontrol')
	streamingBody = response["payload"]
	jsonState = json.loads(streamingBody.read())
	logger.info(jsonState)
 
	return {'statusCode': 200, 'body': json.dumps(jsonState), 'headers': {'Content-Type': 'application/json'}}
	

