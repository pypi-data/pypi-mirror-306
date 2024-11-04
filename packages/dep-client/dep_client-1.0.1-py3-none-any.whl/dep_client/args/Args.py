import argparse

class Args():
    # parser: argparse instance
    def addArguments(parser):
        parser.add_argument("--ip", "-i", type=str, required=True, help="IP address of destination")
        parser.add_argument("--port", "-r", type=int, required=True, help="Port of destination")
        parser.add_argument("--pkgSize", "-k", type=int, default=1321, help="The size of the package which shall be used for exfiltration. Needs to be <= 1321 Bytes")
        parser.add_argument("--msg", "-m", type=str, requred=True, choices=["sim","dim", "dam", "dcm"], help="The message you want to send. Consult README for more information on the message type to choose.")
        parser.add_argument("--uuid", "-u", type=str, required=True, help="uuid4 str, e.g.: 50f437d8-28b7-4c65-9588-eef116a60ae3")
        parser.add_argument("--hash", "-a", type=str, help="sha256 hash of data as hex string")
        parser.add_argument("--path", "-p", type=str, help="(for files) path under which the data is located. (for in memory) path under which the data is saved at exfiltration endpoint")
        parser.add_argument("--size", "-s", type=int, help="size of data in bytes")
        parser.add_argument("--dataState", "-d", type=int, choices=[0,1,2], help="0 = Data is not exfiltrated yet, 1 = Data is already exfiltrated, 2 = Data available under given path but hash differs")