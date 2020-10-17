import ssl
import json

import websocket
import bitstamp.client

import credentials

def cliente():
    return bitstamp.client.Trading(username = credentials.USERNAME,
                                   key = credentials.KEY,
                                   secret = credentials.KEY)


def buy(quantity):
    trading_client = cliente()
    trading_client.buy_market_order(quantity)


def sell(quantity):
    trading_client = cliente()
    trading_client.buy_sell_market_order(quantity)


def on_message(ws, message):
    message = json.loads(message)
    price = message['data']['price']
    print(price)

    if price > 12200:
        sell()
    elif price < 10900:
        buy()
    else:
        print('Wait...')


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    print('Open')

    json_subscribe = """
{
    "event": "bts:subscribe",
    "data": {
        "channel": "live_trades_btcusd"
        }
}
    """

    ws.send(json_subscribe)


if __name__ == "__main__":
    ws = websocket.WebSocketApp("wss://ws.bitstamp.net",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})  # Ignore SSL certified

