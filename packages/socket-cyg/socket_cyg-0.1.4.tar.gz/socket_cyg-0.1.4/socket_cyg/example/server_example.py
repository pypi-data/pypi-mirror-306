"""server_example."""
import asyncio

from socket_cyg.socket_server_asyncio import CygSocketServerAsyncio


if __name__ == '__main__':
    server = CygSocketServerAsyncio()
    asyncio.run(server.run_socket_server())
