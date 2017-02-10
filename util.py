from config import Config
import hashlib
import random
import base64
from datetime import datetime
from functools import reduce


class Util():
    @staticmethod
    def ucenter_aucode(str='', is_encode=True, key=Config.UC_UCKEY, expiry=0):
        """
        uc的加密
        :param str:
        :param is_encode:
        :param key:
        :param expiry:
        :return:
        """
        ckeyLength = 4;

        if (str == ''):
            return ''
        str_byte = str.encode(Config.UC_CHARSET)
        key_byte = key.encode(Config.UC_CHARSET)

        keyMD5 = Util.MD5Tobytes(key_byte)
        key_A = Util.MD5Tobytes(keyMD5[:16])
        key_B = Util.MD5Tobytes(keyMD5[16:])
        key_C = Util.random_bytes(ckeyLength) if is_encode else str_byte[:ckeyLength]

        crytkey = key_A + Util.MD5Tobytes(key_A + key_C)

        str_byte = Util.getCKey(expiry, ckeyLength, is_encode, str_byte, key_B)

        box=[i for i in range(256)]
        rndkey=[crytkey[i%len(crytkey)] for i in range(256)]

        j=0
        for i in range(256):
           j=(j+box[i]+rndkey[i])%256
           box[i], box[j] = box[j], box[i]
        result=[]
        a, j = 0, 0
        for i in range(len(str_byte)):
            a = (a + 1) % 256
            j = (j + box[a]) % 256
            box[a], box[j] = box[j], box[a]
            result.append(str_byte[i] ^ (box[(box[a] + box[j]) % 256]))
        result=bytes(result)

        if not is_encode :
            if (int(result[:10]) == 0 or int(result[:10]) -  datetime.utcnow().timestamp() > 0) \
                    and result[10:26] == Util.MD5(result[26:] + key_B)[:16]:
                return result[26:]
            else:
                return ''
        else:
            return key_C.decode(Config.UC_CHARSET) + Util.base64decode_tostr(result).replace('=', '')

    @classmethod
    def getCKey(cls,expiry, ckeyLength, is_encode, str_byte, key_B):
        if is_encode:
            temp_bytes = b''
            if (expiry != 0):
                temp_bytes = str(expiry + datetime.utcnow().timestamp()).encode(Config.UC_CHARSET)
            else:
                temp_bytes = Util.encode("0000000000")
                str_byte = temp_bytes +Util.MD5Tobytes(str_byte+key_B)[:16]+ str_byte
            pass
        else:
            while len(str_byte) % 4 != 0:
                str_byte += b'='  # 末尾补=,在base64中末尾=是无意义的
            bs64_byte = str_byte[ckeyLength:]
            str_byte = base64.b64decode(bs64_byte)

        return str_byte

    @staticmethod
    def encode(str_input):
        """
        Until中混合着bytes和str,和大量的加法操作很麻烦,而且encode时候必须用Config.charset
        :param self:
        :param str:
        :return:
        """
        if isinstance(str_input, str):
            return str_input.encode(Config.UC_CHARSET)
        elif isinstance(str_input,bytes):
            return str_input
        else:
            raise TypeError('输入参数类型未知')
        pass

    @staticmethod
    def MD5(src_str):
        """

        :param src_str: 被加密的字符串或者byte数组
        :return: MD5字符串 字节
        """
        if isinstance(src_str, str):
            result = hashlib.md5(src_str.encode(Config.UC_CHARSET))
        elif isinstance(src_str, bytes):
            result = hashlib.md5(src_str)
        return result.hexdigest()  # hexdigest返回字符串,16进制数字

    @staticmethod
    def MD5Tobytes(src_str):
        return Util.MD5(src_str).encode()

    @staticmethod
    def random_bytes(count):
        strlist = []
        letters = '1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
        for i in range(count):
            #strlist.append(random.choice(letters))
            strlist.append('a')
        return bytes(''.join(strlist), Config.UC_CHARSET)

    @classmethod
    def base64encode_tostr(self,str):
        """
        base64加密
        :param str:
        :type str str
        :return: 加密后的字符串形式
        """
        str_bytes=Util.encode(str)
        return base64.b64encode(str_bytes).decode()

    @classmethod
    def base64decode_tostr(self,data):
        return base64.b64encode(data).decode(Config.UC_CHARSET)

