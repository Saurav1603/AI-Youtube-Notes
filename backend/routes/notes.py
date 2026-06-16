from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from services.notes_service import generate_notes_from_url
from typing import Optional

router = APIRouter()

class NotesResponse(BaseModel):
    success: bool
    notes: Optional[str] = None
    is_metadata_fallback: Optional[bool] = False
    error: Optional[str] = None

@router.get("/notes", response_model=NotesResponse)
async def get_notes(url: str = Query(..., description="YouTube video URL")):
    try:
        notes, is_metadata = generate_notes_from_url(url)
        return {"success": True, "notes": notes, "is_metadata_fallback": is_metadata}
    except ValueError as ve:
        # Client errors (e.g., invalid URL, no transcript)
        return {"success": False, "error": str(ve)}
    except Exception as e:
        # Server/API errors
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
