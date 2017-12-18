
class base58(object):
    _B58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

    @classmethod
    def from_int(cls,i):
        output = ''
        while i > 0:
            i,r = divmod(i,58)
            output = output + cls._B58[r]
        return output[::-1]

    @classmethod
    def to_int(cls,b58str):
        print b58str
        output = 0
        for c in b58str:
            if c not in cls._B58:
                return None
            i = cls._B58.index(c)
            output = output * 58 + i
    
        return output


