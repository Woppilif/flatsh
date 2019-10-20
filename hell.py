
import asyncio
import websockets
from websockets.exceptions import InvalidStatusCode, ConnectionClosedError
import time
import json

async def hello():
    async with websockets.connect("ws://5.63.152.213/ws/chat/1/") as websocket:
        print("Listening....")
        greeting = await websocket.recv()
        greeting = greeting.replace("'", "\"")
        greeting = json.loads(greeting)
        print(greeting['message'])
        await websocket.send("Hello world!")

 
async def Run():
    while True:
        try:
            await hello()
        except ConnectionClosedError:
            print("Disconnected! Trying to reconnect!")
            time.sleep(5)
        except InvalidStatusCode:
            print("InvalidStatusCode! Trying to connect to server.....!")
            time.sleep(5)
        except ConnectionRefusedError:
            print("ConnectionRefusedError! Trying to connect to server.....!")
            time.sleep(5)
        
asyncio.get_event_loop().run_until_complete(Run())