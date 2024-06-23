import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/events")
async def handle_event(request: Request):
    try:
        logging.info(f"Received request: {request}")
        events = await request.json()
        logging.info(f"Received events: {events}")
        for event in events:
            # Process each event
                #logging.info(f"Received event: {event}")
                print(f"Received event: {event}")
                
        return JSONResponse({content = events}, status_code=200)
    except Exception as e:
        print(f"Error processing event: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.options("/api/events")
async def options_event(request: Request):
    webhook_request_origin = request.headers.get("WebHook-Request-Origin")
    webhook_request_rate = request.headers.get("WebHook-Request-Rate")

    if not webhook_request_origin:
        return PlainTextResponse(content="Missing WebHook-Request-Origin header", status_code=400)

    response_headers = {
        "Allow": "POST",
        "WebHook-Allowed-Origin": webhook_request_origin,
    }

    if webhook_request_rate:
        response_headers["WebHook-Allowed-Rate"] = webhook_request_rate
    else:
        response_headers["WebHook-Allowed-Rate"] = "*"

    return PlainTextResponse(content="OK", status_code=200, headers=response_headers)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/ok")
async def ok_endpoint():
    return {"message": "ok"}
