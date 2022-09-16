import uvicorn
from fastapi import FastAPI
from app.database import Base, engine
from app.api import router_ip
from app.api import router_dns
from app.api import router_file
from app.api import router_url

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router_ip)
app.include_router(router_dns)
app.include_router(router_file)
app.include_router(router_url)


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
