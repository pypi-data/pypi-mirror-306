class Util():
    def sendFileWithEcho(client, icmpType, pkgSize, filePath):
        with open(filePath, "rb") as f:
                while True:
                    data = f.read(pkgSize)
                    if not data:
                        client.sendEchoMessage(icmpType, "file_end")
                        break
                    client.sendEchoMessage(icmpType, data)