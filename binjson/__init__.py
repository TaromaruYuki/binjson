from .ByteTypes import *
from typing import IO

class __BinJsonFile:
    def __init__(self, file_bytes: bytes):
        self.file_bytes = file_bytes
        self.iterator = iter(file_bytes) 
        self.end = False
        self.pos = 0

        self.advance()

    def advance(self):
        try:
            self.value = next(self.iterator)
            self.pos += 1
            return self.value
        except StopIteration:
            self.end = True
            return None

def __get_byte_from_type(value: any) -> bytes:
    if isinstance(value, str):
        return STRING_TYPE.to_bytes(1, "little")
    elif isinstance(value, int):
        return INT_TYPE.to_bytes(1, "little")

def __get_length(value: int):
    # TODO: Find a better way to do this.
    if value <= 255:
        return 1
    else: 
        raise Exception("Value is too long.")

def __encode_value(value: any):
    if isinstance(value, int):
        length = __get_length(value)
        return value.to_bytes(length, "little")
    elif isinstance(value, str):
        return value.encode("UTF-8")

def dump(obj: dict, fp: IO):
    output = b""

    for key, value in obj.items():
        output += KEY.to_bytes(1, "little")
        output += key.encode("UTF-8")
        output += KEY_END.to_bytes(1, "little")
        output += __get_byte_from_type(value)
        output += __encode_value(value)
        output += END_TYPE.to_bytes(1, "little")

    if fp.mode != "wb":
        raise Exception(f"Expected mode 'wb' but got '{fp.mode}'")

    fp.write(output)

def read(fp: IO):
    if fp.mode != "rb":
        raise Exception(f"Expected mode 'rb' but got '{fp.mode}'")

    file = __BinJsonFile(fp.read())
    obj = {}

    while not file.end:
        if file.value != KEY:
            raise Exception(f"Expected key at position {file.pos}")
        file.advance()

        key = ""
        while file.value != KEY_END:
            key += chr(file.value)
            file.advance()
        file.advance()

        if file.value == STRING_TYPE:
            file.advance()
            value = ""
            while file.value != END_TYPE:
                value += chr(file.value)
                file.advance()
        elif file.value == INT_TYPE:
            file.advance()
            # This can only get values from 0x00 to 0xFF.
            # Find a better way to load this.
            value = file.value
            file.advance()

        obj[key] = value
        file.advance()

    return obj