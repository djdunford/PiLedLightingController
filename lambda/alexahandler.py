# -*- coding: utf-8 -*-

# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Amazon Software License (the "License"). You may not use this file except in
# compliance with the License. A copy of the License is located at
#
#    http://aws.amazon.com/asl/
#
# or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, express or implied. See the License for the specific
# language governing permissions and limitations under the License.

import boto3
import json
import logging
from alexa.skills.smarthome import AlexaResponse
import colorsys

logger = logging.getLogger("alexa")
logger.setLevel(logging.DEBUG)
iotClient = boto3.client('iot-data', region_name='eu-west-1') # TODO remove hardcode reference to region

def lambda_handler(request, context):

    # Dump the request for logging - check the CloudWatch logs
    logger.debug('lambda_handler request  -----')
    logger.debug(json.dumps(request))

    if context is not None:
        logger.debug('lambda_handler context  -----')
        logger.debug(context)

    # Validate we have an Alexa directive
    if 'directive' not in request:
        aer = AlexaResponse(
            name='ErrorResponse',
            payload={'type': 'INVALID_DIRECTIVE',
                     'message': 'Missing key: directive, Is the request a valid Alexa Directive?'})
        return send_response(aer.get())

    # Check the payload version
    payload_version = request['directive']['header']['payloadVersion']
    if payload_version != '3':
        aer = AlexaResponse(
            name='ErrorResponse',
            payload={'type': 'INTERNAL_ERROR',
                     'message': 'This skill only supports Smart Home API version 3'})
        return send_response(aer.get())

    # Crack open the request and see what is being requested
    name = request['directive']['header']['name']
    namespace = request['directive']['header']['namespace']

    # Handle the incoming request from Alexa based on the namespace

    if namespace == 'Alexa.Authorization':
        if name == 'AcceptGrant':
            # Note: This sample accepts any grant request
            # In your implementation you would use the code and token to get and store access tokens
            grant_code = request['directive']['payload']['grant']['code']
            grantee_token = request['directive']['payload']['grantee']['token']
            aar = AlexaResponse(namespace='Alexa.Authorization', name='AcceptGrant.Response')
            return send_response(aar.get())

    if namespace == 'Alexa.Discovery':
        if name == 'Discover':
            adr = AlexaResponse(namespace='Alexa.Discovery', name='Discover.Response')
            capability_alexa = adr.create_payload_endpoint_capability()
            capability_alexa_powercontroller = adr.create_payload_endpoint_capability(
                interface='Alexa.PowerController',
                supported=[{'name': 'powerState'}],
                proactively_reported=False,
                retrievable=False
            )
            capability_alexa_colorcontroller = adr.create_payload_endpoint_capability(
                interface='Alexa.ColorController',
                supported=[{'name': 'color'}],
                proactively_reported=False,
                retrievable=False
            )
            adr.add_payload_endpoint(
                friendly_name='Den Lights', # TODO remove hardcoded friendly name
                endpoint_id='thomas-den-lights', # TODO removed hardcoded endpoint_id
                capabilities=[capability_alexa, capability_alexa_powercontroller, capability_alexa_colorcontroller])
            return send_response(adr.get())

    if namespace == 'Alexa.PowerController':
        # Note: This sample always returns a success response for either a request to TurnOff or TurnOn
        endpoint_id = request['directive']['endpoint']['endpointId']
        power_state_value = 'OFF' if name == 'TurnOff' else 'ON'
        correlation_token = request['directive']['header']['correlationToken']

        # Check for an error when setting the state
        state_set = set_device_state(endpoint_id=endpoint_id, state='powerState', value=power_state_value)
        if not state_set:
            return AlexaResponse(
                name='ErrorResponse',
                payload={'type': 'ENDPOINT_UNREACHABLE', 'message': 'Unable to reach endpoint database.'}).get()

        apcr = AlexaResponse(correlation_token=correlation_token)
        apcr.add_context_property(namespace='Alexa.PowerController', name='powerState', value=power_state_value)
        return send_response(apcr.get())

    if namespace == 'Alexa.ColorController' and name == 'SetColor':
        # Note: This sample always returns a success response for either a request to TurnOff or TurnOn
        endpoint_id = request['directive']['endpoint']['endpointId']
        correlation_token = request['directive']['header']['correlationToken']

        # Check for an error when setting the state
        color_set = set_color_state(endpoint_id=endpoint_id, state='color', value=request['directive']['payload']['color'])
        if not color_set:
            return AlexaResponse(
                name='ErrorResponse',
                payload={'type': 'ENDPOINT_UNREACHABLE', 'message': 'Unable to reach endpoint database.'}).get()

        apcr = AlexaResponse(correlation_token=correlation_token)
        apcr.add_context_property(namespace='Alexa.ColorController', name='color', value=request['directive']['payload']['color'])
        return send_response(apcr.get())


def send_response(response):
    # TODO Validate the response
    logger.debug('lambda_handler response -----')
    logger.debug(json.dumps(response))
    return response


def set_device_state(endpoint_id, state, value):
    if value == "ON":
        payload = {"state":{"desired":{"status":"TRIGGER","sequence":3}}}
    else:
        payload = {"state":{"desired":{"status":"TRIGGER","sequence":100}}}

    # TODO replace hardcoded thing name
    response = iotClient.update_thing_shadow(thingName='ThomasBedroomLEDcontrol',payload=json.dumps(payload))
    streamingBody = response["payload"]
    jsonState = json.loads(streamingBody.read())
    logger.info(jsonState)

    # TODO replace with correct return code - currently returns true for success in all cases
    return True

def set_color_state(endpoint_id, state, value):
    h = float(value['hue'])
    s = float(value['saturation'])
    v = float(value['value'])
    r, g, b = [int(c*255) for c in colorsys.hsv_to_rgb(h,s,v)]
    logger.debug("Setting Colour HSV "+str(h)+","+str(s)+","+str(v)+" RGB "+str(r)+","+str(g)+","+str(b))
    payload = {"state":{"desired":{"status":"SETCOLOUR","colour":{"r":r,"g":g,"b":b}}}}

    # TODO replace hardcoded thing name
    response = iotClient.update_thing_shadow(thingName='ThomasBedroomLEDcontrol',payload=json.dumps(payload))
    streamingBody = response["payload"]
    jsonState = json.loads(streamingBody.read())
    logger.info(jsonState)

    # TODO replace with correct return code - currently returns true for success in all cases
    return True
