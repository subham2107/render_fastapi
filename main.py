from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
import logging

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def event_processing_middleware(request: Request, call_next):
    if request.url.path == "/api/events" and request.method == "POST":
        try:
            logging.info(f"Received request: {request}")
            events = await request.json()
            logging.info(f"Received events: {events}")
            for event in events:
                if event.get('eventType') == 'Microsoft.EventGrid.SubscriptionValidationEvent':
                    validation_code = event['data']['validationCode']
                    validation_response = {
                        "validationResponse": validation_code
                    }
                    logging.info(f"Received subscription validation event. Validation code: {validation_code}")
                    logging.info(f"Received event: {event}")
                    print(f"Received event: {event}")
                    return JSONResponse(content=validation_response, status_code=200)
        except Exception as e:
            logging.error(f"Error processing event: {e}")
            return JSONResponse(content={"error": "Invalid event data"}, status_code=400)
    
    response = await call_next(request)
    return response


@app.post("/api/events")
async def handle_event(request: Request):
    return JSONResponse(content={"message": "Event processed"}, status_code=200)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/ok")
async def ok_endpoint():
    return {"message": "ok"}
