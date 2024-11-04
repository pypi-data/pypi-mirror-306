import sys
import argparse

from npdep_http_client.args.Args import Args
from npdep_http_client.util.Util import Util
from npdep_http_client.output.Output import Output
from npdep_http_client.type.RequestType import RequestType
from npdep_http_client.client.Client import Client

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

    client = Client(args.ip, args. port)

    # Get request type
    requestType = RequestType.VALUES[args.mode]

    if(requestType == RequestType.FILE):
        Util.sendFileWithHttpRequest(client, args.pkgSize, args.path, args.filePath)
    elif(requestType == RequestType.PAYLOAD):
        client.sendHttpRequest(s=None, path=args.path, payload=args.payload)
    

    out.printExecutionTime()


if __name__ == "__main__":
    sys.exit(main())
