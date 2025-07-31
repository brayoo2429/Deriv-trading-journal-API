import asyncio
import websockets
import json
import requests
from flask import Flask, jsonify
from threading import Thread

app = Flask(__name__)

# ✅ Your Make.com webhook URL
WEBHOOK_URL = "https://hook.us2.make.com/ct0iist3vs538xomm027874bw92e3yfh"

@app.route('/')
def home():
    return "✅ API is live!"

@app.route('/trades')
def get_trades():
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(fetch_trades())

        # ✅ Send trade data to Make.com webhook
        requests.post(WEBHOOK_URL, json=result)

        return jsonify(result)
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"error": str(e)})

async def fetch_trades():
    uri = "wss://ws.deriv.com/websockets/v3"
    async with websockets.connect(uri) as websocket:
        # ✅ Authorize
        await websocket.send(json.dumps({
            "authorize": "86YW4KgrodfDcL5"  # Your demo token
        }))
        await websocket.recv()  # Wait for response

        # ✅ Get last 5 trades
        await websocket.send(json.dumps({
            "statement": 1,
            "limit": 5,
            "description": 1
        }))
        response = await websocket.recv()
        return json.loads(response)

def run_flask():
    app.run(host="0.0.0.0", port=10000)

if __name__ == '__main__':
    # ✅ Start Flask server in a separate thread
    Thread(target=run_flask).start()
