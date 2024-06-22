import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
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

@app.middleware("http")
async def event_processing_middleware(request: Request, call_next):
    if request.url.path == "/api/events" and request.method == "POST":
        try:
            logger.info("Received request")
            events = await request.json()
            logger.info(f"Received events: {events}")

            if not isinstance(events, list):
                raise ValueError("Event data should be a list of events")

            for event in events:
                if 'eventType' not in event:
                    raise ValueError("Event type missing in event data")
                if event.get('eventType') == 'Microsoft.EventGrid.SubscriptionValidationEvent':
                    validation_code = event['data'].get('validationCode')
                    validation_url = event['data'].get('validationUrl')
                    
                    if not validation_code:
                        raise ValueError("Validation code missing in event data")
                    
                    if validation_url:
                        # Asynchronous (manual) validation
                        async with httpx.AsyncClient() as client:
                            validation_response = await client.get(validation_url)
                            if validation_response.status_code != 200:
                                raise HTTPException(status_code=500, detail="Manual validation failed")
                        logger.info(f"Manual validation successful for URL: {validation_url}")
                    
                    # Synchronous validation response
                    validation_response = {
                        "validationResponse": validation_code
                    }
                    logger.info(f"Received subscription validation event. Validation code: {validation_code}")
                    return JSONResponse(content=validation_response, status_code=200)
        except Exception as e:
            logger.error(f"Error processing event: {e}")
            return JSONResponse(content={"error": "Invalid event data", "detail": str(e)}, status_code=400)
    
    response = await call_next(request)
    return response

@app.post("/api/events")
async def handle_event(request: Request):
    return JSONResponse(content={"message": "Event processed"}, status_code=200)

@app.options("/api/events")
async def options_event():
    return JSONResponse(content={"message": "Options request processed"}, status_code=200)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/ok")
async def ok_endpoint():
    return {"message": "ok"}
