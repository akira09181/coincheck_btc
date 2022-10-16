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
    ticker = coincheck.fetch_ticker(symbol='BTC/JPY')
    last = float(ticker['info']['last'])*0.97
    buy = int(last*0.97)
    sell = int(last*1.03)
    print(ticker['info']['last'])
    balance = coincheck.fetchBalance()
    print(balance['info']['jpy'])
    order = coincheck.create_order(
        symbol='BTC/JPY',
        type='limit',
        side='buy',
        amount=0.00004,
        price=buy,
    )
    order2 = coincheck.create_order(
        symbol='BTC/JPY',
        type='limit',
        side='sell',
        amount=0.0039,
        price=sell,
    )
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
            # "location": ip.text.replace("\n", "")
        }),
    }
