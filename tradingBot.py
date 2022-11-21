#import required libraries
import websocket, json, pprint, numpy, talib, requests

#socket for the binance kline stream
SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"
#preset values for the rsi calculations
RSI_Period = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
TRADE_SYMB = 'ETHUSD'
TRADE_AMT = 1

id = 100000

#array to store all the closes for each candlestick
all_closes = []

#boolean to store whether you are in the position to buy or sell
in_position = False

#when the connection is opened
def on_open(ws):
    print("opened connection")

#when the connection is closed
def on_close(ws):
    print("closed connection")  

#when a message is recieved, all major logic is in this function
def on_message(ws, message):
    #access the global variable
    global all_closes

    #print that the message is recieved along with the message itself
    print("receieved message")
    json_message = json.loads(message)
    pprint.pprint(json_message)

    #get the candle values received (open, close, time, etc.)
    candle = json_message['k']
    #from the candle values, store whether candle is closed or not
    closed = candle['x']
    #from the candle values, store the closing value
    closed_value = candle['c']

    #only run if the candle is closed
    if closed:
        print("candle closed at {}".format(closed_value))
        all_closes.append(float(closed_value))
        print("Closed values: ")
        print(all_closes)

        if len(all_closes) > RSI_Period:
            closes = numpy.array(all_closes)
            rsi = talib.RSI(closes, RSI_Period)
            print("all rsis")
            print(rsi)
            last_rsi = rsi[-1]

            if last_rsi > RSI_OVERBOUGHT:
                if in_position:
                    print("sell")
                    id = id + 1
                    #put sell logic here
                else:
                    print("nothing to sell")
            
            if last_rsi < RSI_OVERSOLD:
                if in_position:
                    print("oversold but you already own")
                else:
                    print("buy")
                    #put buy logic here
                    id = id + 1

ws = websocket.WebSocketApp(SOCKET, on_open= on_open, on_close=on_close, on_message=on_message)

ws.run_forever()