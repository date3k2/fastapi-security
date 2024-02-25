import itertools
import requests

import string
import time
username = "bxkozw"

url = "http://127.0.0.1:8000/login"

start = time.time()
for x in itertools.product(string.digits, repeat=3):
    password = "".join(x)
    response = requests.post(
        url,
        json={"username": username, "password": password},
    )
    # print(password, response.status_code, "at", datetime.now())

print("Time:", time.time() - start)
