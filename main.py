import asyncio
import websockets
import json
from flask import Flask, jsonify
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return "API is running ✅"

@app.route('/trades')
def get_trades():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(fetch_trades())
    return result

async def fetch_trades():
    uri = "wss://ws.deriv.com/websockets/v3"
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps({
            "authorize": "86YW4KgrodfDcL5"
        }))
        await websocket.recv()  # Auth response

        await websocket.send(json.dumps({
            "statement": 1,
            "limit": 5,
            "description": 1
        }))

        response = await websocket.recv()
        return json.loads(response)

def run_flask():
    app.run(host='0.0.0.0', port=10000)

if __name__ == '__main__':
    Thread(target=run_flask).start()
