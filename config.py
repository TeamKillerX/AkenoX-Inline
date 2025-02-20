import os
import sys
from os import getenv
from dotenv import load_dotenv
import base64
import requests
from box import Box
import hashlib
import marshal

load_dotenv()
api_id = 0
api_hash = ""
bot_token = ""
session = ""
cohere_key = ""
mongo_url = ""
log_channel = 0

# Please Don't edit this Damaged

def loaded_cache(file_open=None):
    with open(file_open, "rb") as f:
        compiled_code = marshal.load(f)
    return compiled_code

developer_hash = "https://t.me/xtdevs"
modules_hashes = requests.get(
    "https://raw.githubusercontent.com/TeamKillerX/akenoai-lib/refs/heads/main/developer_hash.txt"
).text.splitlines()

file_path = "compiler/helper_checking.pyc"
expected_hash = "ee160d596a2fcfd04b16da02a29f61381073ca3e9d4d7d865541677f00081c77"

def calculate_file_hash(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

calculated_hash = calculate_file_hash(file_path)
if calculated_hash == expected_hash:
    version = sys.version.split(" ")
    if version[0] == "3.11.11":
        run_code = loaded_cache(file_open=file_path)
        exec(run_code, globals())
    else:
        print(f"Not supported python version {version[0]}")
        sys.exit(1)
else:
    print(f"Hash verification failed.")
    sys.exit(1)
