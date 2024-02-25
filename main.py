from rate_limit import *
from fastapi import FastAPI, Depends, Body
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from models import UserBase, Users
from sqlmodel import Session, select
from db import get_session, init_db
from hash import check_password
from fastapi.responses import JSONResponse
from datetime import datetime
import argparse

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
parser = argparse.ArgumentParser(description="FastAPI Rate Limiting")
parser.add_argument("--limit", action="store_true", help="Enable rate limiting")

args = parser.parse_args()

if args.limit:
    app.add_middleware(RateLimitingMiddleware)
else:
    print("Rate limiting is disabled")

# oauth_scheme = OAuth2PasswordBearer(tokenUrl="login")
# @app.on_event("startup")
# def on_startup():
#     init_db()


@app.get("/")
async def read_root():
    return {"message": "Hello World"}


@app.post("/login")
async def login(
    user: Annotated[UserBase, Body()], session: Session = Depends(get_session)
):
    statement = select(Users).where(Users.username == user.username)
    result = session.exec(statement).first()
    if result:
        if check_password(result.password, user.password):
            result.loggedIn = 1
            result.loggedAt = datetime.now()
            session.add(result)
            session.commit()
            session.refresh(result)

            return {"result": "success", "userId": result.userId}
        else:
            return JSONResponse(status_code=404, content={"result": "failed"})
    else:
        return JSONResponse(status_code=404, content={"result": "failed"})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
