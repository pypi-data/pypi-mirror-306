from typing import Union
import os
try:
    import base4
except ImportError:
    os.system('pip install base4')
else:
    print("")
base4_CHARSET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./♕♡•~/?!;: ديفل ضصثقفغعهخحجشسيبلاتنمكطذءؤرىةوزظدال"
base4_DICT = {v: i for i, v in enumerate(base4_CHARSET)}
def d4encode(buf: bytes) -> bytes:
    res = ""
    buflen = len(buf)
    for i in range(0, buflen & ~1, 2):
        x = (buf[i] << 8) + buf[i + 1]
        e, x = divmod(x, 45 * 45)
        d, c = divmod(x, 45)
        res += base4_CHARSET[c] + base4_CHARSET[d] + base4_CHARSET[e]
    if buflen & 1:
        d, c = divmod(buf[-1], 45)
        res += base4_CHARSET[c] + base4_CHARSET[d]
    return res.encode()
def d4decode(s: Union[bytes, str]) -> bytes:
    try:
        if isinstance(s, str):
            buf = [base4_DICT[c] for c in s.rstrip("\n")]
        elif isinstance(s, bytes):
            buf = [base4_DICT[c] for c in s.decode()]
        else:
            raise TypeError("Type must be 'str' or 'bytes'")
        buflen = len(buf)
        if buflen % 3 == 1:
            raise ValueError("Invalid base4 string")
        res = []
        for i in range(0, buflen, 3):
            if buflen - i >= 3:
                x = buf[i] + buf[i + 1] * 45 + buf[i + 2] * 45 * 45
                if x > 0xFFFF:
                    raise ValueError
                res.extend(divmod(x, 256))
            else:
                x = buf[i] + buf[i + 1] * 45
                if x > 0xFF:
                    raise ValueError
                res.append(x)
        return bytes(res)
    except (ValueError, KeyError, AttributeError):
        raise ValueError("Invalid base4 string")