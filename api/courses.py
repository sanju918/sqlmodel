import fastapi
from fastapi import Path, Query
from api.models.user_model import User
import uuid
from typing import List, Optional

router = fastapi.APIRouter()
