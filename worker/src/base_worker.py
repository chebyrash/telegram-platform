import asyncio
import json
import logging
import time

import aiohttp


class BaseWorker(object):
    def __init__(self, endpoint: str, process_message: callable = None):
        with open("config.json") as file:
            self._config = json.loads(file.read())["base_worker"]
            file.close()

        self._pool_url = "http://{0}:{1}{2}".format(
            self._config["pool_host"],
            self._config["pool_port"],
            endpoint,
        )
        self._server_connection = None
        self._process_message = process_message

    @staticmethod
    def _log(message: str):
        logging.info("[LINK] %s" % message)

    def run(self):
        self._log("STARTING")

        asyncio.get_event_loop().create_task(self.connect_to_server())

    async def send_response_to_server(self, message: dict):
        await self._server_connection.send_json(message)

    async def send_error_to_server(self, error: str):
        await self.send_response_to_server({"error": error})

    async def connect_to_server(self):
        try:
            self._server_connection = await aiohttp.ClientSession().ws_connect(
                url=self._pool_url,
                autoping=True,
            )

            self._log("Connected")

            await self.process_connection(self._server_connection)
        except Exception as e:
            self._log("Error: %s" % e)

            self._log("Could not connect")

        self._log("Reconnecting")

        time.sleep(self._config["timeout"])
        await self.connect_to_server()

        self._log("Exiting")

    async def process_connection(self, connection: aiohttp.ClientWebSocketResponse):
        async for message in connection:
            if message.type == aiohttp.WSMsgType.TEXT:
                self._log("Server sent %s" % message.data)

                if self._process_message is not None:
                    await self._process_message(json.loads(message.data))

            else:
                self._log("Disconnected with exception %s" % connection.exception())
                await connection.close()
                break
