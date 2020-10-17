import ssl
import json

import websocket


def buy():
    pass


def sell():
    pass


def on_message(ws, message):
    message = json.loads(message)
    price = message['data']['price']
    print(price)

    if price > 9000:
        sell()
    elif price < 8000:
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

