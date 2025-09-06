import aiohttp
import asyncio
import logging
import websockets
import names
from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK
from get_currency import main as get_currency
from aiopath import AsyncPath
import aiofiles

logging.basicConfig(level=logging.INFO)


class Server:
    clients = set()

    async def log_to_file(self, message:str):
        async with aiofiles.open("log.txt", "a") as f:
            await f.write(message + "\n")
    async def register(self, ws: WebSocketServerProtocol):
        ws.name = names.get_full_name()
        self.clients.add(ws)
        logging.info(f'{ws.remote_address} connects')

    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        logging.info(f'{ws.remote_address} disconnects')

    async def send_to_clients(self, message: str):
        if self.clients:
            [await client.send(message) for client in self.clients]

    async def ws_handler(self, ws: WebSocketServerProtocol):
        await self.register(ws)
        try:
            await self.distrubute(ws)
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(ws)

    async def get_currency_rates_text(self, arg1=1, arg2=None):
        # Create a formatted string of current currency rates
        message = await get_currency(arg1, arg2)
        return message

    async def distrubute(self, ws: WebSocketServerProtocol):
        async for message in ws:
            new_message = message.strip()
            split_message = new_message.split(" ")
            if split_message[0] == 'exchange':
                # If message is 'exchange', send currency rates
                if len(split_message) >= 3:
                    rates_message = await self.get_currency_rates_text(split_message[1], split_message[2:])
                elif len(split_message) == 2:
                    rates_message = await self.get_currency_rates_text(split_message[1])
                else:
                    rates_message = await self.get_currency_rates_text()
                await self.log_to_file(f"The exchange function has been called by {ws.name} \n with the result {rates_message}")
                await ws.send(str(rates_message))
            else:
                await self.send_to_clients(f"{ws.name}: {message}")


async def main():
    server = Server()
    async with websockets.serve(server.ws_handler, 'localhost', 8080):
        await asyncio.Future()  # run forever

if __name__ == '__main__':
    asyncio.run(main())
