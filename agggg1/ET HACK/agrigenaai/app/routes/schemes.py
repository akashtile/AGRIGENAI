from fastapi import APIRouter
from app.models.schemas import SchemeRequest, SchemeResponse
from app.services.rag import retrieve_schemes

router = APIRouter()

@router.post("/search", response_model=SchemeResponse)
def search_schemes(request: SchemeRequest):
    result = retrieve_schemes(
        query=request.query,
        state=request.state,
        crop=request.crop,
        farmer_category=request.farmer_category
    )
    return SchemeResponse(**result)
