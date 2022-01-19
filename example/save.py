import binjson
import json

obj = {
    "name": "Doggo",
    "bio": "dog.",
    "coins": 58
}

with open("files/test.bin", "wb") as f:
    binjson.dump(obj, f)

with open("files/test.json", "w") as f:
    json.dump(obj, f, indent=0)