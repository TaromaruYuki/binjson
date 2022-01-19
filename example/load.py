import binjson

with open("files/test.bin", "rb") as f:
    data = binjson.read(f)

print(data)