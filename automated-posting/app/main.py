from fastapi import FastAPI
from app.schemas import PostingRequest, PostingResponse
from app.services.posting_service import post_to_all_platforms

app = FastAPI(
    title="Automated Multi-Platform Posting API",
    description="Publishes one validated message to configured platforms.",
    version="1.0.0",
)

@app.get("/")
async def health():
    return {"status": "ok", "message": "Posting API is running"}

@app.post("/posting", response_model=PostingResponse)
async def posting(payload: PostingRequest):
    results = await post_to_all_platforms(payload.message)
    return PostingResponse(
        success=any(item.status == "success" for item in results),
        results=results,
    )
