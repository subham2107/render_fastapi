# from typing import Optional

from fastapi import FastAPI, Request, HTTPException

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
            print(f"Received event: {event}")
            # Add your custom processing logic here

        return {"status": "success"}
    except Exception as e:
        print(f"Error processing event: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

 