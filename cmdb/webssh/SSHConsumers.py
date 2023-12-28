import json
from threading import Thread
from jwt import decode
from channels.generic.websocket import WebsocketConsumer
import paramiko


class SSHConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ip = None
        self.chan = None
        self.ssh = None

    def connect(self):

        # self.ip = self.scope['url_route']['kwargs']['ip']
        print(self.ip)
        self.accept()
        self._init()

    def disconnect(self, close_code):
        self.chan.close()
        self.ssh.close()

    def get_client(self):
        # p_key = paramiko.RSAKey.from_private_key_file("/root/.ssh/id_rsa")  # ssh免密登录私钥
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # ssh.connect(hostname=self.ip, port=22, username='root', pkey=p_key)
        ssh.connect(hostname='192.168.3.97',username='root', password='Sdls@#$2021', allow_agent=False, look_for_keys=False, timeout=10)


        return ssh

    def loop_read(self):
        while True:
            data = self.chan.recv(32 * 1024)
            if not data:
                self.close(1234)
                break

            self.send(bytes_data=data)

    def _init(self):
        self.send(bytes_data=b'Connecting ...\r\n')

        try:
            self.ssh = self.get_client()
        except Exception as e:
            self.send(bytes_data=f'Exception: {e}\r\n'.encode())
            self.close()
            return

        self.chan = self.ssh.invoke_shell(term='xterm')
        self.chan.transport.set_keepalive(30)

        Thread(target=self.loop_read).start()

    def receive(self, text_data=None, bytes_data=None):
        data = text_data or bytes_data
        if data:
            data = json.loads(data)

            resize = data.get('resize')
            if resize and len(resize) == 2:
                self.chan.resize_pty(*resize)
            else:
                self.chan.send(data['data'])