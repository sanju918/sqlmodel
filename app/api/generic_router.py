import fastapi

router = fastapi.APIRouter()


@router.get("/", tags=["Generic"])
async def root():
    return {"message": "hello world"}
