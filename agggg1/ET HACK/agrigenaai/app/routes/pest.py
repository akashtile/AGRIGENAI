from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.schemas import PestDetectionResponse
from app.services.vision import detect_pest_from_image

router = APIRouter()

@router.post("/detect", response_model=PestDetectionResponse)
async def detect_pest(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are accepted.")

    image_bytes = await file.read()
    result = detect_pest_from_image(image_bytes)
    return PestDetectionResponse(**result)
