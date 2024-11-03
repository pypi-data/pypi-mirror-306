"""socket 客户端."""
import datetime
import os
import socket
import sys
import threading
import logging
from logging.handlers import TimedRotatingFileHandler


class SocketClient:
    """socket 客户端class."""
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s"


    def __init__(self, host="127.0.0.1", port=8000):
        self._logger = logging.getLogger(f"{self.__module__}.{self.__class__.__name__}")
        self._file_handler = None
        self.set_log()

        self._host = host
        self._port = port
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
        """保存日志的日志处理器."""
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
        """日志器."""
        return self._logger

    @property
    def host(self):
        """服务端ip."""
        return self._host

    @host.setter
    def host(self, host):
        """设置连接的服务端ip."""
        self._host = host

    @property
    def port(self):
        """服务端端口号."""
        return self._port

    @port.setter
    def port(self, port):
        """设置要连接的服务端端口号."""
        self._port = port

    @property
    def client(self):
        """客户端socket实例."""
        return self._client

    @client.setter
    def client(self, client: socket):
        """设置客户端socket实例."""
        self._client = client

    def client_open(self):
        """连接服务端."""
        self.client.connect((self.host, self.port))
        self._logger.info("*** 和服务端连接成功 ***")

    def client_close(self):
        """关闭客户端连接."""
        self.client.close()
        self._logger.warning("*** 客户端关闭连接 ***")

    def client_send(self, message: str):
        """客户端发送数据."""
        data = message.encode("UTF-8")
        self.client.sendall(data)
        self._logger.info("*** 客户端发送数据 *** -> data: %s", data)

    def client_receive(self):
        """客户端接收数据."""
        try:
            while True:
                data = self.client.recv(1024)
                if not data:
                    break
                str_data = data.decode("utf-8")
                self._logger.info("*** 客户端接收到服务端数据 *** -> data: %s", str_data)
                self.operations()
        except Exception as e:  # pylint: disable=W0718
            self._logger.warning("*** 出现异常 *** -> 异常信息: %s", str(e))
        finally:
            self.client.close()

    def operations(self):
        """根据服务端发过来的数据进行的操作"""

    def run_receive_thread(self):
        """启动客户端线程, 实时监听服务端发来的数据."""
        thread = threading.Thread(target=self.client_receive, daemon=False)
        thread.start()
