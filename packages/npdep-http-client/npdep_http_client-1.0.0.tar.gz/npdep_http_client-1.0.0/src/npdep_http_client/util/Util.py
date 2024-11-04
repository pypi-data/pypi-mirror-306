import socket

class Util():
    def sendFileWithHttpRequest(client, pkgSize, path, filePath):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((client.ip, client.port))
        with open(filePath, "rb") as f:
                while True:
                    data = f.read(pkgSize)
                    if not data:
                        break
                    client.sendHttpRequest(s, path, data)
        s.close()