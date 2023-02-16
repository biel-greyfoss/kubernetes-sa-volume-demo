from typing import Union

from fastapi import FastAPI
from http import client

app = FastAPI()


@app.get("/")
def read_root():
    return {"Message": "From api"}


def read_token():
    with open("/var/run/secrets/tokens/api-token", "r", encoding="UTF-8") as f:
        service_token = f.readline()
        print(f"read service account token:{service_token}")
        return service_token


@app.get("/call")
def call():
    conn = client.HTTPConnection("app.data-store.svc.cluster.local",8080)

    service_token = read_token()

    headers = {"X-Client-Id": service_token}


    conn.request('GET', '/sensitive',None, headers)

    response = conn.getresponse()
    print(f"response: {response}")
    response_str = response.read().decode()
    print(f"response_str: {response_str}")


    return response_str
