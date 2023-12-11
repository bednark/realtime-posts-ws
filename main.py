import asyncio
import websockets

CLIENTS = set()

async def handler(websocket):
  CLIENTS.add(websocket)
  while True:
    async for message in websocket:
      await broadcast(message)

async def broadcast(message):
  for client in CLIENTS.copy():
    try:
      await client.send(message)
    except websockets.ConnectionClosed:
      CLIENTS.remove(client)

async def main():
  async with websockets.serve(handler, "", 8001):
    await asyncio.Future()

if __name__ == "__main__":
  print('Listening on port 8001')
  asyncio.run(main())