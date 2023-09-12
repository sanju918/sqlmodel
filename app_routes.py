from runserver import app


@app.get("/")
async def root():
    return {"message": "hello world"}
