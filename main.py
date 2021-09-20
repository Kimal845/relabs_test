import uvicorn

from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


app = FastAPI()

templates = Jinja2Templates(directory='templates')


@app.get("/", response_class=HTMLResponse)
async def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    import json
    await websocket.accept()
    id = 0
    while True:
        data = await websocket.receive_text()
        id = id + 1
        response = json.dumps({
            'data': data,
            'id': id
        })

        await websocket.send_json(data=response)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
