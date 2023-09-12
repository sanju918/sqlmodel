import fastapi

router = fastapi.APIRouter()
tag = ["Courses"]


@router.get("/courses", tags=tag)
async def read_courses():
    return {"courses": []}


@router.post("/courses", tags=tag)
async def create_course_api():
    return {"courses": []}


@router.get("/courses/{id}", tags=tag)
async def read_course():
    return {"courses": []}


@router.patch("/courses/{id}", tags=tag)
async def update_course():
    return {"courses": []}


@router.delete("/courses/{id}", tags=tag)
async def delete_course():
    return {"courses": []}


@router.get("/courses/{id}/sections", tags=tag)
async def read_course_sections():
    return {"courses": []}