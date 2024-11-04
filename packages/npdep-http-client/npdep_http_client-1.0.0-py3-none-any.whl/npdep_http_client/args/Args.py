import argparse

class Args():
    # parser: argparse instance
    def addArguments(parser):
        parser.add_argument("--mode", "-m", type=str, choices=["payload", "file"], default="file", help="Client mode: ")
        parser.add_argument("--ip", "-i", type=str, required=True, help="IP address of destination")
        parser.add_argument("--port", "-p", type=int, required=True, help="Port of destination")
        parser.add_argument("--pkgSize", "-k", type=int, default=1200, help="Paket size of file")
        parser.add_argument("--path", "-t", type=str, default="/", help="Path for HTTP request")
        parser.add_argument("--filePath", "-e", type=str, default=".", help="Path to the file which shall be send. Mode: file")
        parser.add_argument("--payload", "-a", type=str, default="", help="Payload to be send. Mode: payload")