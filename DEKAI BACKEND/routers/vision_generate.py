from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from PIL import Image
import io

from oath2 import get_current_user
from model import dekaiImg0 

router = APIRouter(
    prefix="/vision",
    tags=["vision"]
)


@router.post("/analyze")
async def analyze_image(
    image: UploadFile = File(...),
    current_user = Depends(get_current_user)
):
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid image type")

    contents = await image.read()
    pil_image = Image.open(io.BytesIO(contents)).convert("RGB")

    caption =dekaiImg0.generate_caption(pil_image)

    return {
        "engine": "dekai-img-0",
        "caption": caption
    }
