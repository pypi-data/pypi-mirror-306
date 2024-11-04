class Args():
    # parser: argparse instance
    def addArguments(parser):
        parser.add_argument("--mode", "-o", type=str, choices=["payload", "file"], default="file", help="Client mode")
        parser.add_argument("--msg", "-m", type=str, required=True, choices=["echo_req", "echo_rep"], help="Message you want to send. Consult README for more information.")
        parser.add_argument("--ip", "-i", type=str, required=True, help="IP address of destination")
        parser.add_argument("--port", "-p", type=int, default=0, help="Port of destination")
        parser.add_argument("--pkgSize", "-k", type=int, default=1200, help="Paket size of file")
        parser.add_argument("--filePath", "-e", type=str, default=".", help="Path to the file which shall be send. Mode: file")
        parser.add_argument("--payload", "-a", type=str, default="", help="Payload to be send. Mode: payload")