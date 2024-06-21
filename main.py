from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import logging

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/ok")
async def ok_endpoint():
    return {"message": "ok"}

@app.post("/api/events")
async def handle_event(request: Request):
    try:
        events = await request.json()
        for event in events:
            # Process each event
            #   if event.get('eventType') == 'Microsoft.EventGrid.SubscriptionValidationEvent':
            #     validation_code = event['data']['validationCode']
            #     validation_response = {
            #         "validationResponse": validation_code
            #     }
            #     logging.info(f"Received subscription validation event. Validation code: {validation_code}")
                logging.info(f"Received event: {event}")
                print(f"Received event: {event}")
                # return JSONResponse(content=validation_response, status_code=200)
                

        return JSONResponse({"status": "success"}, status_code=200)
    except Exception as e:
        print(f"Error processing event: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

 

        