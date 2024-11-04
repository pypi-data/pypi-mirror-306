import socket

class Client():
    def __init__(self, ip, port) -> None:
        self.ip = ip
        self.port = port

    def sendHttpRequest(self, s, path, payload, host=None):
        _host = self.ip
        if(host != None):
            _host = host
        header = f"GET {path} HTTP/1.1\r\nHost: {_host}\r\nConnection: Close\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\n\r\n"
        
        request = bytearray(0)        
        request.extend(header.encode("utf-8"))

        # Check type of payload and add the byte to request
        if(type(payload) == str):
            request.extend(payload.encode("utf-8"))
        elif(type(payload) == int):
            request.extend(payload.to_bytes())
        else:
            request.extend(payload)

        if(s == None):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.ip, self.port))
            s.sendall(request)
            s.close()
        else:
            s.sendall(request)