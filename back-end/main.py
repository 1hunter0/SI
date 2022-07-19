import uvicorn
from fastapi import FastAPI
from starlette.responses import RedirectResponse

app = FastAPI()

#根据搜索内容重定向数据
app.get("search/{data}")
def parse(data):
    # response = RedirectResponse(url=url)
    # return response
    return {"hello world"}

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)