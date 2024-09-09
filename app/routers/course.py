import logging
from fastapi import APIRouter, HTTPException
from ..logger import logger
from ..models import ImageResponse, ImageVariationResponse
from ..services.course import generate_course_summary, generate_image_prompt, generate_image
from ..services.image_variation import generate_image_variations

router = APIRouter(
    # prefix="/course",
    tags=["Course"]
)

@router.get("/course/{course_id}", response_model=ImageResponse,summary= "Create thumbnail from course title, description, and table of contents")
def generate_course_image(course_id: str):
    try:
        final_summary = generate_course_summary(course_id)
        image_prompt = generate_image_prompt(final_summary)
        image_url = generate_image(image_prompt)
        return {
            "final_summary": final_summary,
            "image_prompt": image_prompt,
            "image_url": image_url
        }
    except Exception as e:
        logger.exception("Error while generating the image")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/variations/course/{course_id}", response_model=ImageVariationResponse,summary= "Generate thumbnail variations from an existing course thumbnail")
def generate_course_image_variations(course_id: str):
    try:
        logger.info(f"Course ID : {course_id}")
        image_urls = generate_image_variations(course_id)
        return ImageVariationResponse(images=image_urls)
    except Exception as e:
        logger.exception("Error while generating the image variations")
        raise HTTPException(status_code=500, detail=str(e))

    