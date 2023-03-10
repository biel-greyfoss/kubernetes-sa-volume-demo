from typing import Union

from fastapi import FastAPI, HTTPException, Request
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from pprint import pprint


app = FastAPI()

config.load_incluster_config()
v1 = client.CoreV1Api()

print("Load k8s config success")



@app.get("/")
def read_root():
    return {"Hello": "I am data-store"}

def verify_token(client_id: str):
    with client.ApiClient() as api_client:
        api_instance = client.AuthenticationV1Api(api_client)
        # Create a V1TokenReview
        body = client.V1TokenReview(
            spec=client.V1TokenReviewSpec(
                audiences=["data-store"],
                token=client_id
            )
        )

    try:
        api_response = api_instance.create_token_review(body)
        pprint(api_response)
        return api_response.status.authenticated
    except ApiException as e:
        print(f"Exception when calling AuthenticationV1Api->create_token_review: {e}\n")
        return False



@app.get("/sensitive")
def sensitive(request: Request):
    client_id = request.headers.get("X-Client-Id", None)

    print(f"client_id is : {client_id}")

    if not client_id:
        raise HTTPException(
            status_code=401,
            detail="X-Client-Id not supplied",
        )

    if verify_token(client_id):
        return {"Message": "Hello from data store. You have been authenticated"}
    else:
        return {"Message": "Invalid token"}