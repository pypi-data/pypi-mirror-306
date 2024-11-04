from dep_common.msg.MessageType import MessageType

class MessageFactory:
    def __init__(self) -> None:
        pass
    
    '''
        - SystemInformationMessage
            - Payload = 18 Byte
                - systemId: 16 Byte
                -  pkgSize:  2 Byte
    ''' 
    # uuid - bytes - a uuid in bytes representation
    def createSystemInformationMessage(self, uuid, pkgSize):
        payload = bytearray(0)
        payload.extend(uuid)

        # Create Payload: pkgSize
        payload.extend(pkgSize.to_bytes(2, "big"))

        msg = self.__createMsg(MessageType.SYSTEM_INFORMATION_MESSAGE, payload)

        return msg
    
    '''
        - DataInformationMessage
            - Payload = 316 Byte
                - systemId:  16 Byte
                -   sha256:  32 Byte
                -     size:   8 Byte -> 18,4 Exabyte file size
                -     path: 260 Byte
    '''
    #        uuid - bytes - a uuid in bytes representation
    # sha256_hash - bytes - SHA256 hash in bytes of the data to be transfered
    #        path -   str - (for files)     path under which the data is located 
    #                       (for in memory) path under which the data is saved at exfiltration endpoint
    #        size -   int - size of data in bytes
    def createDataInformationMessage(self, uuid, sha256_hash, path, size):
         # Create Payload: systemId
        payload = bytearray(0)
        payload.extend(uuid)

        # Create Payload: sha256
        payload.extend(sha256_hash)

        # Create Payload: size
        payload.extend(size.to_bytes(8, "big"))

        # Create Payload: path
        payload.extend(path.encode(encoding="utf-8"))

        # Create Message
        msg = self.__createMsg(MessageType.DATA_INFORMATION_MESSAGE, payload)

        return msg
    
    '''
        - DataAcknowledgeMessage
            - Payload: 49 Byte
                -  systemId:  16 Byte
                -    sha256:  32 Byte
                - dataState:   1 Byte
    '''
    #        uuid -  bytes - A uuid in bytes representation
    # sha256_hash -  bytes - SHA256 hash in bytes of the data this message corresponds to
    #   dataState -    int - 0 = Data is not exfiltrated yet
    #                        1 = Data is already exfiltrated 
    #                        2 = Data available under given path but hash differs
    def createDataAcknowledgeMessage(self, uuid, sha256_hash, dataState):
        # Create Payload: systemId
        payload = bytearray(0)
        payload.extend(uuid)

        # Create Payload: sha256
        payload.extend(sha256_hash)

        # Create Payload: dataState
        payload.extend(dataState.to_bytes(1, "big"))

        # Create Message
        msg = self.__createMsg(MessageType.DATA_ACKNOWLEDGE_MESSAGE, payload)

        return msg
    

    '''
        - DataContentMessage
            - Payload: depends on size of data field
                - systemId:        16 Byte
                -   sha256:        32 Byte
                -  package:         8 Byte
                -     data: max. 1321 Byte
    '''
    #        uuid -  bytes - A uuid in bytes representation
    # sha256_hash -  bytes - SHA256 hash of the data to be transfered
    #       pkgNr -    int - Number of the package
    #        data -  bytes - Actual data content 
    def createDataContentMessage(self, uuid, sha256_hash, pkgNr, data):
        # Create Payload: systemId
        payload = bytearray(0)
        payload.extend(uuid)

        # Create Payload: sha256
        payload.extend(sha256_hash)

        # Create Payload: package
        payload.extend(pkgNr.to_bytes(8, "big"))

        # Create Payload: data
        payload.extend(data)

        # Create Message
        msg = self.__createMsg(MessageType.DATA_CONTENT_MESSAGE, payload)

        return msg
    
    '''
        - DEP - Data Exfiltration Protocol
            - Header
                -   type: 1 Byte
                - length: 2 Byte
    '''
    def __createMsg(self, msgType, payload):
        msg = bytearray()
        # Convert message type to bytes - header.type
        msg.extend(msgType.to_bytes(1, "big"))
        # Convert length of payload to bytes - header.length
        msg.extend(len(payload).to_bytes(2, 'big'))
        msg.extend(payload)
        return msg