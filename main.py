
from fastapi import FastAPI
from service.database import db_engine, Base
from router import user as user_router, tracked_coin as coin_router

Base.metadata.create_all(bind=db_engine)

app = FastAPI()


app.include_router(user_router.router)
app.include_router(coin_router.router)

@app.get("/api")
def read_root():
    return {"Hello": "World"}