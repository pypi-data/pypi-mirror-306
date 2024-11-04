import sys
import argparse

from dep_common.converter.Converter import Converter as DEPConverter
from dep_common.msg.MessageType import MessageType as DEPMessageType

from dep_client.args.Args import Args
from dep_client.util.Util import Util
from dep_client.client.Client import Client
from dep_client.output.Output import Output

def main(args_=None):
    """The main routine."""
    if args_ is None:
        args_ = sys.argv[1:]

    parser = argparse.ArgumentParser()
    Args.addArguments(parser)
    args = parser.parse_args()

    # Creates Output instance for printing header and footer of console output
    out = Output()
    out.printHeader()

    # Create client
    c = Client(args.ip, args.port, args.pkgSize)

    # Get message type
    msgType = DEPMessageType.VALUES[args.msg]
    # Handle msg type
    b_systemId = DEPConverter.uuidStrToBytes(args.uuid)
    if(msgType == DEPMessageType.SYSTEM_INFORMATION_MESSAGE):
        c.sendSystemInformationMessage(b_systemId)
    elif(msgType == DEPMessageType.DATA_INFORMATION_MESSAGE):
        b_sha256Hash = DEPConverter.sha256HashStrToBytes(args.hash)
        c.sendDataInformationMessage(b_systemId, b_sha256Hash, args.path, args.size)
    elif(msgType == DEPMessageType.DATA_ACKNOWLEDGE_MESSAGE):
        b_sha256Hash = DEPConverter.sha256HashStrToBytes(args.hash)
        c.sendDataAcknowledgeMessage(b_systemId, b_sha256Hash, args.dataState)
    elif(msgType == DEPMessageType.DATA_CONTENT_MESSAGE):
        b_sha256Hash = DEPConverter.sha256HashStrToBytes(args.hash)
        Util.sendFileWithDataContentMessage(c, args.ip, args.port, args.pkgSize, args.path, b_systemId, b_sha256Hash)
        
    else:
        print("Wrong Message Type provided!")

    out.printExecutionTime()


if __name__ == "__main__":
    sys.exit(main())
