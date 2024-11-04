import sys
import argparse

from npdep_icmp_client.args.Args import Args
from npdep_icmp_client.util.Util import Util
from npdep_icmp_client.output.Output import Output
from npdep_icmp_client.client.Client import Client
from npdep_icmp_client.type.IcmpType import IcmpType
from npdep_icmp_client.type.RequestType import RequestType

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

    client = Client(args.ip, args.port)

    # Get request type
    echoMsgType = IcmpType.VALUES[args.msg]
    requestType = RequestType.VALUES[args.mode]

    if(requestType == RequestType.FILE):
        Util.sendFileWithEcho(client, echoMsgType, args.pkgSize, args.filePath)
    elif(requestType == RequestType.PAYLOAD):
            client.sendEchoMessage(echoMsgType, args.payload)

    out.printExecutionTime()


if __name__ == "__main__":
    sys.exit(main())
