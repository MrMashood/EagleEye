import os
import io
import asyncio
import time
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from PIL import Image
from app import verifier
from logger import (
    log_incoming_request, log_image_fetch, log_image_fetch_success,
    log_image_fetch_error, log_gemini_request, log_gemini_response,
    log_gemini_error, log_result_summary
)
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Product Image Verification API",
    description="Verifies if product images match their descriptions using Google Gemini.",
    version="1.0.0"
)


# ── Request / Response models ────────────────────────────────────────────────

class MediaItem(BaseModel):
    id: int
    mediaUrl: str
    mediaType: str


class ProductRequest(BaseModel):
    id: int
    title: str
    description: str
    catgoryName: str
    media: List[MediaItem]


class ImageResult(BaseModel):
    mediaId: int
    mediaUrl: str
    confidence: int
    verdict: str
    reasoning: str
    success: bool
    error: str | None = None


class VerificationResponse(BaseModel):
    productId: int
    title: str
    category: str
    overallVerdict: str
    overallConfidence: int
    results: List[ImageResult]


# ── Helpers ──────────────────────────────────────────────────────────────────

async def fetch_image(client: httpx.AsyncClient, item: MediaItem) -> Image.Image:
    log_image_fetch(item.id, item.mediaUrl)
    response = await client.get(item.mediaUrl, timeout=10)
    response.raise_for_status()
    log_image_fetch_success(item.id, item.mediaUrl)
    return Image.open(io.BytesIO(response.content)).convert("RGB")


async def process_media_item(
    client: httpx.AsyncClient,
    item: MediaItem,
    category: str,
    combined_title: str
) -> ImageResult:
    try:
        image = await fetch_image(client, item)

        log_gemini_request(item.id, category, combined_title)
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None, verifier.verify_image, image, category, combined_title
        )

        if result["success"]:
            log_gemini_response(item.id, result["confidence"], result["verdict"])
        else:
            log_gemini_error(item.id, result.get("error", "Unknown error"))

        return ImageResult(
            mediaId=item.id,
            mediaUrl=item.mediaUrl,
            confidence=result["confidence"],
            verdict=result["verdict"],
            reasoning=result["reasoning"],
            success=result["success"],
            error=result.get("error")
        )

    except httpx.HTTPError as e:
        log_image_fetch_error(item.id, item.mediaUrl, str(e))
        return ImageResult(
            mediaId=item.id,
            mediaUrl=item.mediaUrl,
            confidence=0,
            verdict="Error",
            reasoning=f"Failed to fetch image: {e}",
            success=False,
            error=str(e)
        )
    except Exception as e:
        log_gemini_error(item.id, str(e))
        return ImageResult(
            mediaId=item.id,
            mediaUrl=item.mediaUrl,
            confidence=0,
            verdict="Error",
            reasoning=f"Unexpected error: {e}",
            success=False,
            error=str(e)
        )


def aggregate_verdict(results: List[ImageResult]) -> tuple[str, int]:
    successful = [r for r in results if r.success]
    if not successful:
        return "Error", 0
    avg_confidence = round(sum(r.confidence for r in successful) / len(successful))
    verdict_priority = {"Mismatch": 0, "Uncertain": 1, "Match": 2, "Unknown": 1}
    overall = min(successful, key=lambda r: verdict_priority.get(r.verdict, 1)).verdict
    return overall, avg_confidence


# ── Endpoint ─────────────────────────────────────────────────────────────────

@app.post("/verify", response_model=VerificationResponse)
async def verify_product(product: ProductRequest):
    if not product.media:
        raise HTTPException(status_code=400, detail="No media items provided.")

    start_time = time.time()
    combined_title = f"{product.title} — {product.description}"
    category = product.catgoryName

    log_incoming_request(product.id, product.title, category, len(product.media))

    async with httpx.AsyncClient() as client:
        tasks = [
            process_media_item(client, item, category, combined_title)
            for item in product.media
        ]
        image_results = await asyncio.gather(*tasks)

    overall_verdict, overall_confidence = aggregate_verdict(list(image_results))

    duration_ms = (time.time() - start_time) * 1000
    log_result_summary(product.id, overall_verdict, overall_confidence, duration_ms)

    return VerificationResponse(
        productId=product.id,
        title=product.title,
        category=category,
        overallVerdict=overall_verdict,
        overallConfidence=overall_confidence,
        results=list(image_results)
    )


# ── Health check ─────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {"status": "ok"}