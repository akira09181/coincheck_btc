import json
import boto3
import ccxt
# import requests
REGION = 'ap-northeast-1'


def lambda_handler(event, context):
    ssm = boto3.client('ssm', region_name=REGION)
    response = ssm.get_parameters(
        Names=[
            'coincheck-api-key',
            'coincheck-secret',
        ],
        WithDecryption=True
    )
    apikey = response['Parameters'][0]['Value']
    apisecret = response['Parameters'][1]['Value']
    coincheck = ccxt.coincheck({'apiKey': apikey, 'secret': apisecret})
    print(coincheck.fetch_ticker(symbol='BTC/JPY'))
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
            # "location": ip.text.replace("\n", "")
        }),
    }
