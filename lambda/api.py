import json
import boto3
import logging

logger = logging.getLogger("api")
logger.setLevel(logging.DEBUG)
iotClient = boto3.client('iot-data', region_name='eu-west-1')

def showsequence(event, context):    
    logger.debug("Received event: " + json.dumps(event, indent=2))
    try:
        seq = int(event['pathParameters']['sequence'])
    except ValueError:
        raise Exception("Invalid sequence parameter - must be a non-zero integer")
    logger.debug("Checking integer: " + str(seq))
    if seq == 0:
        raise Exception("Invalid sequence parameter - must be non-zero")
    logger.debug("Valid non-zero integer confirmed")
        
    logger.info("Executing showsequence command: " + event['pathParameters']['sequence'])
    payload = {"state":{"desired":{"status":"TRIGGER","sequence":seq}}}
    response = iotClient.update_thing_shadow(thingName='ThomasBedroomLEDcontrol',payload=json.dumps(payload))
    streamingBody = response["payload"]
    jsonState = json.loads(streamingBody.read())
    logger.info(jsonState)
    # TODO replace CORS domain with environment variable
    headers = {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': 'https://lights.debsanddarren.com'}
    return {'statusCode': 200, 'body': json.dumps(jsonState), 'headers': headers}

def off(event, context):    
    logger.info("Executing off command:")
    payload = {"state":{"desired":{"status":"TRIGGER","sequence":100}}}
    response = iotClient.update_thing_shadow(thingName='ThomasBedroomLEDcontrol',payload=json.dumps(payload))
    streamingBody = response["payload"]
    jsonState = json.loads(streamingBody.read())
    logger.info(jsonState)
    # TODO replace CORS domain with environment variable
    headers = {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': 'https://lights.debsanddarren.com'}
    return {'statusCode': 200, 'body': json.dumps(jsonState), 'headers': headers}

def state(event, context):
    logger.info("Executing state command (returns state)")
    response = iotClient.get_thing_shadow(thingName='ThomasBedroomLEDcontrol')
    streamingBody = response["payload"]
    jsonState = json.loads(streamingBody.read())
    logger.debug(jsonState)
    # TODO replace CORS domain with environment variable
    headers = {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': 'https://lights.debsanddarren.com'}
    return {'statusCode': 200, 'body': json.dumps(jsonState), 'headers': headers}
