from fastapi import FastAPI #https://fastapi.tiangolo.com/tutorial/first-steps/

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}