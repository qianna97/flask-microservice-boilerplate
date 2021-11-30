import bcrypt as bc

from .Core import caches
from AesEverywhere import aes256


def getCache(domain, id):
    return caches.get(domain + "-" + str(id))


def setCache(domain, id, data):
    return caches.set(domain + "-"  + str(id), data)


def updateCache(domain, id, new_data):
    caches.delete(domain + "-" + str(id))
    return caches.set(domain + "-" + str(id), new_data)


def deleteCache(domain, id):
    return caches.delete(domain + "-" + str(id))


def findKeysCache(domain):
    k_prefix = caches.cache.key_prefix
    keys = caches.cache._write_client.keys(k_prefix + '*')
    keys = [k.decode('utf8') for k in keys]
    keys = [k.replace(k_prefix, '') for k in keys]
    result = list(filter(lambda x: (domain in x), keys))
    return result


def encryptBC(key):
    if isinstance(key, str):
        key = bytes(key, 'utf-8')

    return str(bc.hashpw(key, bc.gensalt()), 'utf8')


def checkBC(passwd, check):
    if isinstance(passwd, str) and isinstance(check, str):
        check  = bytes(check, 'utf-8')
        passwd = bytes(passwd, 'UTF-8')

    return bc.hashpw(check, passwd) == passwd


def encryptAES(values, salt):
    val       = json.dumps(values)
    encrypted = aes256.encrypt(val, salt)
    return str(encrypted, 'utf-8')


def decryptAES(values, salt):
    decrypted = aes256.decrypt(values, salt)
    return json.loads(decrypted)