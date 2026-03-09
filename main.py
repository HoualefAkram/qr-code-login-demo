from fastapi import FastAPI, HTTPException
from datetime import datetime, timedelta
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


uuids = dict()


# Helper Func
def retrieve_uuid(uuid: str):
    result = uuids.get(uuid)

    if not result:
        return None

    if datetime.now() > result["expires_at"]:
        uuids.pop(uuid)
        return None

    return result


# Sent by the TV after generating the QR Code
@app.put("/login")
def save_uuid(uuid: str):
    result = retrieve_uuid(uuid)
    if result:
        return result
    time_to_add = timedelta(minutes=2)
    response = {
        "state": "pending",
        "expires_at": datetime.now() + time_to_add,
    }
    uuids[uuid] = response
    return response


# Sent by the mobile after logging in
@app.patch("/login")
def save_token(uuid: str, token: str):
    if not retrieve_uuid(uuid):
        raise HTTPException(status_code=404, detail="Login info not found")
    uuids[uuid]["state"] = "accepted"
    uuids[uuid]["token"] = token
    return {"status": "ok"}


# Fetched by the TV to login in
@app.get("/login")
def get_token(uuid: str):
    result = retrieve_uuid(uuid)
    if not result:
        raise HTTPException(status_code=404, detail="Code expired or not found")
    return result
