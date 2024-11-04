import hashlib

class Hash():
    def getSha256Hash(path):
        with open(path, "rb") as f:
            sha256_hash = hashlib.sha256()
            chunk = f.read(8192)
            while chunk:
                sha256_hash.update(chunk)
                chunk = f.read(8192)
        return sha256_hash.digest()