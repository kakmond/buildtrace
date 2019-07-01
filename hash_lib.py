import hashlib

# encrypt file to hash 
def sha256sum(filename):
    h = hashlib.sha256()
    with open(filename, 'rb', buffering=0) as f:
        for b in iter(lambda : f.read(128*1024), b''):
            h.update(b)
    return h.hexdigest()

# encrypt string to hash 
def sha256string(string):
    h = hashlib.sha256(string.encode('utf-8'))
    return h.hexdigest()