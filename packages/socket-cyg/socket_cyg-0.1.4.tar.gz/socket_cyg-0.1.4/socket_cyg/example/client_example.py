"""client_example."""
from socket_cyg.socket_client import SocketClient


if __name__ == '__main__':
    client = SocketClient()
    client.client_open()
    client.run_receive_thread()
