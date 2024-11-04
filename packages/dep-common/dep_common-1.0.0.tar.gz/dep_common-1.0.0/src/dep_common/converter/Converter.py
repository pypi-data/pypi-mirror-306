import uuid

class Converter():
    # uuid - uuid.uuid4 - a 16 Byte uuid4
    # ---
    # Returns given uuid as 16 bytes 
    def uuidToBytes(uuid_):
        return uuid_.bytes

    # uuidStr - str - a uuid4 repr.: 50f437d8-28b7-4c65-9588-eef116a60ae3
    # ---
    # Returns given uuid as 16 bytes
    def uuidStrToBytes(uuidStr):
        return uuid.UUID(uuidStr).bytes

    # uuidBytes - bytes - a uuid4 as 16 bytes
    # ---
    # Returns given uuid bytes as uuid4 string: 50f437d8-28b7-4c65-9588-eef116a60ae3
    def bytesToUuidStr(uuidBytes):
        return str(uuid.UUID(bytes=uuidBytes))
    
    # hashStr - str - A sha256 hash string
    # ---
    # Returns given sha256 string as 32 bytes
    def sha256HashStrToBytes(hashStr):
        return bytes.fromhex(hashStr)
    
    # bytes_ - bytes - bytes
    # ---
    # Returns given bytes as hex str
    def bytesToHex(bytes_):
        return bytes_.hex()