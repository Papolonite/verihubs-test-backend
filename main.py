
from fastapi import FastAPI
from service.database import db_engine, Base
from router import user as user_router, tracked_coin as coin_router

Base.metadata.create_all(bind=db_engine)

app = FastAPI(
    description='''
    API to Track user coin based on Coincap v2
    
    ## Users
    Handle the User of System
    
    ## Tracked Coins
    Handle Tracking Coin for User
    ''',
    openapi_tags=[
        {
            'name' : 'users',
            'description' : 'Consist of APIs related to user operation.'
        },
        {
            'name' : 'tracked_coin',
            'description': 'Handle Tracked Coin Operation. Login first to use these APIs'
        }
    ]
)


app.include_router(user_router.router)
app.include_router(coin_router.router)

@app.get("/api")
def read_root():
    return {"Hello": "World"}