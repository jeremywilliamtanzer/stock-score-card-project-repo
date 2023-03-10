from fastapi import FastAPI

api = FastAPI()

# define a root `/` endpoint
@api.get("/")
def index():
    return {"ok": "API connected"}
