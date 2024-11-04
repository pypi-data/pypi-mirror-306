import uuid

from dep_common.msg.MessageType import MessageType as DEPMessageType

from dep_reader.util.Util import Util

class Reader():
    def __init__(self, packageSize = 1321) -> None:
        self.packageSize = packageSize

    def setPackageSize(self, newValue):
        self.packageSize = newValue

    # msg - bytes - the dep message in bytes
    def processMessage(self, msg):
        # Cut message in header and payload
        header = msg[0:3:1]

        # Parse information of the header
        h_type = header[0:1:1]
        h_length = header[1:3:1]
        h_type_int = int.from_bytes(h_type, "big")
        h_length_int = int.from_bytes(h_length, "big")

        # Get payload
        payload = msg[3:h_length_int+1:1]

        # Pass the payload to the message type related processing function
        if(h_type_int == DEPMessageType.SYSTEM_INFORMATION_MESSAGE):
            result = self.processSystemInformationMessage(payload)
        elif(h_type_int == DEPMessageType.DATA_INFORMATION_MESSAGE):
            result = self.processDataInformationMessage(payload)
        elif(h_type_int == DEPMessageType.DATA_ACKNOWLEDGE_MESSAGE):
            result = self.processDataAcknowledgeMessage(payload)
        elif(h_type_int == DEPMessageType.DATA_CONTENT_MESSAGE):
            result = self.processDataContentMessage(payload)
        else:
            print("Message Type incorrect!")

        return result

    def processSystemInformationMessage(self, payload):
        p_systemId = payload[0:16:1]
        p_pkgSize =  payload[16:18:1]
        systemId = uuid.UUID(bytes=p_systemId)
        packageSize = int.from_bytes(p_pkgSize, "big")

        return {
            "msgType": DEPMessageType.SYSTEM_INFORMATION_MESSAGE,
            "systemId": systemId,
            "pkgSize": packageSize
        }

    def processDataInformationMessage(self, payload):
        p_systemId = payload[0:16:1]
        p_sha256 = payload[16:48:1]
        p_size = payload[48:56:1]
        p_size_int = int.from_bytes(p_size, "big")
        p_pkgs_int = Util.getNoOfPackages(p_size_int / self.packageSize)
        p_path = payload[56:len(payload)+1:1]

        return {
            "msgType": DEPMessageType.DATA_INFORMATION_MESSAGE,
            "systemId": uuid.UUID(bytes=p_systemId),
            "sha256": p_sha256.hex(),
            "size": p_size_int,
            "noOfPkgs": p_pkgs_int,
            "path": p_path.decode("utf-8")
        }
        
    def processDataAcknowledgeMessage(self, payload):
        p_systemId = payload[0:16:1]  
        p_sha256 = payload[16:48:1]
        p_dataState = payload[48:49:1]
        p_dataState_int = int.from_bytes(p_dataState, "big")

        return {
            "msgType": DEPMessageType.DATA_ACKNOWLEDGE_MESSAGE,
            "systemId": uuid.UUID(bytes=p_systemId),
            "sha256": p_sha256.hex(),
            "dataState": p_dataState_int
        }

    def processDataContentMessage(self, payload):
        p_systemId = payload[0:16:1]
        p_sha256 = payload[16:48:1]
        p_pkgNr = payload[48:56:1]
        p_data = payload[56:len(payload)+1:1]
                
        return {
            "msgType": DEPMessageType.DATA_CONTENT_MESSAGE,
            "systemId": uuid.UUID(bytes=p_systemId),
            "sha256": p_sha256.hex(),
            "packageNr": int.from_bytes(p_pkgNr, "big"),
            "data": p_data
        }