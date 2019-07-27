import json
import boto3
import logging

logger = logging.getLogger("api")
logger.setLevel(logging.DEBUG)
iotClient = boto3.client('iot-data', region_name='eu-west-1')

def showsequence(event, context):    
    logger.debug("Received event: " + json.dumps(event, indent=2))
    seq = int(event['pathParameters']['sequence']
    if seq == 0:
        raise Exception("Invalid sequence parameter - not an integer"
        
    logger.info("Executing showsequence command: " + event['pathParameters']['sequence'])
    payload = {"state":{"desired":{"status":"TRIGGER","sequence":seq}}}
    response = client.update_thing_shadow(thingName='ThomasBedroomLEDcontrol',payload=json.dumps(payload))
    streamingBody = response["payload"]
    jsonState = json.loads(streamingBody.read())
    logger.info(jsonState)
    return {'statusCode': 200, 'body': json.dumps(jsonState), 'headers': {'Content-Type': 'application/json'}}

def state(event, context):
    logger.info("Executing state command (returns state)")
    response = iotClient.get_thing_shadow(thingName='ThomasBedroomLEDcontrol')
    streamingBody = response["payload"]
    jsonState = json.loads(streamingBody.read())
    logger.debug(jsonState)
    return {'statusCode': 200, 'body': json.dumps(jsonState), 'headers': {'Content-Type': 'application/json'}}
