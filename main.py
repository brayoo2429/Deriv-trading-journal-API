import asyncio
import websockets
import json
import requests
from flask import Flask, jsonify
from threading import Thread

# ✅ Your Make.com webhook URL
webhook_url = "https://hook.us2.make.com/ct0iist3vs538xomm027874bw92e3yfh"

app = Flask(__name__)

@app.route('/')
def home():
    return "API is running ✅"

@app.route('/trades')
def get_trades():
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(fetch_trades())

        # ✅ Send to Make.com webhook
        requests.post(webhook_url, json=result)

        return jsonify(result)
    except Exception as e:
        print(f"❌ Error occurred: {e}")
        return jsonify({"error": str(e)})

async def fetch_trades():
    uri = "wss://ws.deriv.com/websockets/v3"
    async with websockets.connect(uri) as websocket:
        # ✅ Step 1: Authorize
        await websocket.send(json.dumps({
            "authorize": "86YW4KgrodfDcL5"  # Demo API token
        }))
        await websocket.recv()  # Wait for authorization response

        # ✅ Step 2: Request last 5 trades
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
    thread = Thread(target=run_flask)
    thread.start()
