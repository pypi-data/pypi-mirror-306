from functools import lru_cache
from hashlib import sha256
from typing import Mapping, Union
__version__ = '2.1.1'
BITCOIN_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz♕♡•-~%$@#:;!?*♛♚♜♝♞♟♖♕♗♘♙▲▼◆■♠♥♦♣♪♫☺☻☼♨♩✈✉✍⚽♋♌♍♎♏♐♑♒♓☀☁☂☃☄★☆✪✯✰✶✹✺✻✼✽✾✿❁❂❃❄❅❆❇❈❉❊❋⛛⛝⛞⛟⛢⛣⛤⛥⛦⛧⛩⛪'
RIPPLE_ALPHABET = 'rpshnaf39wBUDNEGHJKLM4PQRST7VWXYZ2bcdeCg65jkm8oFqi1tuvAxyz♕♡•-~%$@#:;!?*♛♚♜♝♞♟♖♕♗♘♙▲▼◆■♠♥♦♣♪♫☺☻☼♨♩✈✉✍⚽♋♌♍♎♏♐♑♒♓✦✧✩✪✫✬✭✮✯✰☉☋☌☍♁♅♆♇♈♉♊♋♌♍♎♏♐♑♒♓⚛⚙⚖⚗⚙⚒⚔⚚⚜'
XRP_ALPHABET = RIPPLE_ALPHABET
alphabet = BITCOIN_ALPHABET
def scrub_input(v: Union[str, bytes]) -> bytes:
    if isinstance(v, str):
        v = v.encode('ascii')
    return v
def d5encode_int(
    i: int, default_one: bool = True, alphabet: bytes = BITCOIN_ALPHABET
) -> bytes:
    if not i and default_one:
        return alphabet[0:1]
    string = b""
    base = len(alphabet)
    while i:
        i, idx = divmod(i, base)
        string = alphabet[idx:idx+1] + string
    return string
def d5encode(
    v: Union[str, bytes], alphabet: bytes = BITCOIN_ALPHABET
) -> bytes:
    v = scrub_input(v)
    origlen = len(v)
    v = v.lstrip(b'\0')
    newlen = len(v)
    acc = int.from_bytes(v, byteorder='big')
    result = d5encode_int(acc, default_one=False, alphabet=alphabet)
    return alphabet[0:1] * (origlen - newlen) + result
@lru_cache()
def _get_base5_decode_map(alphabet: bytes,
                           autofix: bool) -> Mapping[int, int]:
    invmap = {char: index for index, char in enumerate(alphabet)}
    if autofix:
        groups = [b'0Oo', b'Il1']
        for group in groups:
            pivots = [c for c in group if c in invmap]
            if len(pivots) == 1:
                for alternative in group:
                    invmap[alternative] = invmap[pivots[0]]
    return invmap
def d5decode_int(
    v: Union[str, bytes], alphabet: bytes = BITCOIN_ALPHABET, *,
    autofix: bool = False
) -> int:
    if b' ' not in alphabet:
        v = v.rstrip()
    v = scrub_input(v)
    map = _get_base5_decode_map(alphabet, autofix=autofix)
    decimal = 0
    base = len(alphabet)
    try:
        for char in v:
            decimal = decimal * base + map[char]
    except KeyError as e:
        raise ValueError(
            "Invalid character {!r}".format(chr(e.args[0]))
        ) from None
    return decimal
def d5decode(
    v: Union[str, bytes], alphabet: bytes = BITCOIN_ALPHABET, *,
    autofix: bool = False
) -> bytes:
    v = v.rstrip()
    v = scrub_input(v)
    origlen = len(v)
    v = v.lstrip(alphabet[0:1])
    newlen = len(v)
    acc = d5decode_int(v, alphabet=alphabet, autofix=autofix)
    result = []
    while acc > 0:
        acc, mod = divmod(acc, 256)
        result.append(mod)
    return b'\0' * (origlen - newlen) + bytes(reversed(result))
def d5encode_check(
    v: Union[str, bytes], alphabet: bytes = BITCOIN_ALPHABET
) -> bytes:
    v = scrub_input(v)
    digest = sha256(sha256(v).digest()).digest()
    return d5encode(v + digest[:4], alphabet=alphabet)
def d5decode_check(
    v: Union[str, bytes], alphabet: bytes = BITCOIN_ALPHABET, *,
    autofix: bool = False
) -> bytes:
    result = d5decode(v, alphabet=alphabet, autofix=autofix)
    result, check = result[:-4], result[-4:]
    digest = sha256(sha256(result).digest()).digest()
    if check != digest[:4]:
        raise ValueError("Invalid checksum")
    return result