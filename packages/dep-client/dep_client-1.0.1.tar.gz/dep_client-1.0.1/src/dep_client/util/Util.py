import sys
import socket

class Util():
    def sendFileWithDataContentMessage(client, ip, port, pkgSize, path, b_systemId, b_sha256Hash):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        with open(path, "rb") as f:
                counter = 1
                while True:
                    data = f.read(pkgSize)
                    if not data:
                        break
                    client.sendDataContentMessage(s, b_systemId, b_sha256Hash, counter, data)
                    counter = counter + 1
        s.close()

    def sendDataWithDataContentMessage(client, ip, port, pkgSize, data, counter, b_systemId, b_sha256Hash):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        client.sendDataContentMessage(s, b_systemId, b_sha256Hash, counter, data)
        s.close()