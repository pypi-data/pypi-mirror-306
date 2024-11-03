"""异步socket."""
import asyncio
import datetime
import logging
import os
import socket
import sys
from asyncio import AbstractEventLoop
from logging.handlers import TimedRotatingFileHandler
from typing import Union


# pylint: disable=R0801
class CygSocketServerAsyncio:
    """异步socket class."""
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s"

    clients = {}  # 保存已连接的client
    tasks = {}
    loop: AbstractEventLoop = None

    def __init__(self, address="127.0.0.1", port=8000):
        self._address = address
        self._port = port
        self._logger = logging.getLogger(f"{self.__module__}.{self.__class__.__name__}")
        self._file_handler = None
        self.set_log()
        self.queue = asyncio.Queue()

    def set_log(self):
        """设置日志."""
        self.file_handler.setFormatter(logging.Formatter(self.LOG_FORMAT))
        self.file_handler.setLevel(logging.INFO)
        self.logger.addHandler(self.file_handler)
        if sys.version_info.minor == 11:
            logging.basicConfig(level=logging.INFO, encoding="UTF-8", format=self.LOG_FORMAT)
        else:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(logging.Formatter(self.LOG_FORMAT))
            console_handler.setLevel(logging.INFO)
            self.logger.addHandler(console_handler)
            self.logger.setLevel(logging.INFO)

    @property
    def file_handler(self):
        """保存日志的日志器."""
        if self._file_handler is None:
            log_dir = f"{os.getcwd()}/log"
            os.makedirs(log_dir, exist_ok=True)
            file_name = f"{log_dir}/{datetime.datetime.now().strftime('%Y-%m-%d')}_{os.path.basename(os.getcwd())}.log"
            self._file_handler = TimedRotatingFileHandler(
                file_name, when="D", interval=1, backupCount=10, encoding="UTF-8"
            )
        return self._file_handler

    @property
    def logger(self):
        """日志实例."""
        return self._logger

    def operations_return_data(self, data: bytes):
        """操作返回数据."""
        data = data.decode("UTF-8")
        self._logger.warning("*** 回显 *** -> 没有重写 operations_return_data 函数, 默认是回显.")
        return data

    async def socket_send(self, client_connection, data: Union[bytes, str]):
        """发送数据给客户端."""
        if isinstance(data, str):
            data = data.encode("utf-8")
        if client_connection:
            client_ip = client_connection.getpeername()
            await self.loop.sock_sendall(client_connection, data)
            self._logger.info("***发送*** --> %s 发送成功, %s", client_ip, data)
        else:
            self._logger.info("***发送*** --> 发送失败, %s, 未连接", data)

    async def receive_send(self, client_connection: socket.socket):
        """接收发送数据."""
        client_ip = client_connection.getpeername()[0]  # 获取连接客户端的ip
        try:
            while data := await self.loop.sock_recv(client_connection, 1024 * 1024):
                str_data = data.decode("UTF-8")
                self._logger.info("%s", "-" * 60)
                self._logger.info("***Socket接收*** --> %s, 数据: %s", client_ip, str_data)

                commands = str_data.split("@_@")[:-1:]
                self._logger.info("*** 本次接收到指令的个数 *** --> %s", len(commands))

                for command_data in commands:
                    await self.queue.put(command_data)

                while True:
                    if self.queue.qsize() == 0:
                        break
                    command_data = await self.queue.get()
                    if command_data is None:
                        break
                    self._logger.info("*** 从队列中获取一个指令和数据 *** -> %s", command_data)
                    self.queue.task_done()

                    send_data = self.operations_return_data(command_data)  # 这个方法实现具体业务, 需要重写, 不重写回显
                    send_data_byte = send_data.encode("UTF-8")
                    await self.loop.sock_sendall(client_connection, send_data_byte)
                    self._logger.info("***Socket回复*** --> %s, 数据: %s", client_ip, send_data)
                    self._logger.info("%s", "-" * 60)
        except Exception as e:  # pylint: disable=W0718
            self._logger.warning("***通讯出现异常*** --> 异常信息是: %s", e)
        finally:
            self.clients.pop(client_ip)
            self.tasks.get(client_ip).cancel()
            self._logger.warning("***下位机断开*** --> %s, 断开了", client_ip)
            client_connection.close()

    async def listen_for_connection(self, socket_server: socket):
        """异步监听连接."""
        self._logger.info("***服务端已启动*** --> %s 等待客户端连接", socket_server.getsockname())

        while True:
            self.loop = asyncio.get_running_loop()
            client_connection, address = await self.loop.sock_accept(socket_server)
            self._logger.warning("***下位机连接*** --> %s, 连接了", address)

            client_connection.setblocking(False)
            self.clients.update({address[0]: client_connection})
            self.tasks.update({
                address[0]: self.loop.create_task(self.receive_send(client_connection))
            })
            await self.socket_send(client_connection, "^_^")

    async def run_socket_server(self):
        """运行socket服务, 并监听客户端连接."""
        socket_server = socket.socket()
        socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socket_server.setblocking(False)
        socket_server.bind((self._address, self._port))
        socket_server.listen()
        await self.listen_for_connection(socket_server)
