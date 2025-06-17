from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

@app.get("/")
async def index():
    return {"message": "Hello from FastAPI on Vercel"}

handler = Mangum(app)
