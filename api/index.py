from fastapi import FastAPI , Request

app = FastAPI()

@app.get("/")
async def index():
    return {"message": "Hello World"}   