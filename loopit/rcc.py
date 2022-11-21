from calendar import month_name
import socket
import json
import time
import numpy as np

# %%
class Client(object):
    """
     A LocaliteJSON socket client used to communicate with a LocaliteJSON socket server.
    example
    -------
    host = '127.0.0.1'
    port = 6666
    client = Client(True)
    client.connect(host, port).send(data)
    response = client.recv()
    client.close()
    example
    -------
    response = Client().connect(host, port).send(data).recv_close()
    """

    socket = None

    def __init__(self, host, port=1219, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout

    def connect(self):
        "connect wth the remote server"
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.socket.settimeout(self.timeout)

    def close(self):
        "closes the connection"
        self.socket.shutdown(1)
        self.socket.close()
        del self.socket

    def write(self, data):
        packet = data.encode("ascii")
        # print("Writing:", packet)
        self.socket.sendall(packet)
        return self

    def read_byte(self, counter, buffer):
        """read next byte from the TCP/IP bytestream and decode as ASCII"""
        if counter is None:
            counter = 0
        char = self.socket.recv(1).decode("ascii")
        buffer.append(char)
        counter += {"{": 1, "}": -1}.get(char, 0)
        return counter, buffer

    def read(self):
        "parse the message until it is a valid json"
        counter = None
        buffer = []
        while counter != 0:
            counter, buffer = self.read_byte(counter, buffer)
            # print(buffer)
            try:
                response = "".join(buffer)
                # print(response)
                # response = response.replace("ent_sa", "")
                # response = response.replace("\\t", "")
                # response = response.replace("\\u0002", "")
                # print(response)
                return self.decode(response)
            except json.JSONDecodeError as e:
                pass

    def listen(self):
        self.connect()
        msg = self.read()
        self.close()
        return msg

    def decode_one(self, msg: str, index=0):
        try:
            decoded = json.loads(msg)
        except json.JSONDecodeError as e:
            # print("JSONDecodeError: " + msg)
            raise e

        key = list(decoded.keys())[index]
        val = decoded[key]
        return {key: val}

    def decode(self, msg: str):
        try:
            decoded = json.loads(msg)
        except json.JSONDecodeError as e:
            # print("JSONDecodeError: " + msg)
            raise e

        return decoded

    def send(self, msg: str):
        self.connect()
        self.write(msg)
        self.close()

    def request(self, msg='{"ping":"pong"}'):
        self.connect()
        self.write(msg)
        print("Sent:", msg)
        # time.sleep(1)
        msg = self.read()
        print("Received:\n", json.dumps(msg, indent=4))
        self.close()
        return msg


def parse_rtt(input):
    rtt = input.split(",")
    if len(rtt) == 2:
        rtt.append(1)
    else:
        rtt[2] = int(rtt[2])
    return rtt


def crappyhist(a, bins=50, width=140):
    import numpy as np

    h, b = np.histogram(a, bins)

    for i in range(0, bins):
        print(
            "{:12.5f}  | {:{width}s} {}".format(
                b[i], "#" * int(width * h[i] / np.amax(h)), h[i], width=width
            )
        )
    print("{:12.5f}  |".format(b[bins]))