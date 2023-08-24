from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import user


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)

# @app.on_event("startup")
# async def startup():
#     await db.database.connect()

@app.get("/")
async def root():
    return {"message": "Hello World"}

# @app.on_event("shutdown")
# async def shutdown():
#     await db.database.disconnect()
