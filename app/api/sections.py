import fastapi

router = fastapi.APIRouter()

tag = ["Sections"]


@router.get("/sections/{id}", tags=tag)
async def read_section():
    return {"courses": []}


@router.get("/sections/{id}/content-blocks", tags=tag)
async def read_section_content_blocks():
    return {"courses": []}


@router.get("/content-blocks/{id}", tags=tag)
async def read_content_block():
    return {"courses": []}