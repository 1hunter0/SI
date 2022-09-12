import uvicorn
from fastapi import FastAPI
from app.database import Base, engine
from app.api import router_ip

Base.metadata.create_all(bind=engine)
from api.api import router

app = FastAPI()

app.include_router(router_ip)

app.include_router(router)

app.include_router(router)

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
