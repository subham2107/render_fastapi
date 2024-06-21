from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
import logging

app = FastAPI(middleware=[
            Middleware(
            CORSMiddleware,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
            allow_origins=["*"],
            )]
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/ok")
async def ok_endpoint():
    return {"message": "ok"}

@app.post("/api/events")
async def handle_event(request: Request):
    try:
        logging.info(f"Received request: {request}")
        events = await request.json()
        logging.info(f"Received events: {events}")
        for event in events:
            # Process each event
            if event.get('eventType') == 'Microsoft.EventGrid.SubscriptionValidationEvent':
                validation_code = event['data']['validationCode']
                validation_response = {
                    "validationResponse": validation_code
                }
                logging.info(f"Received subscription validation event. Validation code: {validation_code}")
                logging.info(f"Received event: {event}")
                print(f"Received event: {event}")
                return JSONResponse(content=validation_response, status_code=200)
                

        return JSONResponse({"status": "success"}, status_code=200)
    except Exception as e:
        print(f"Error processing event: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

