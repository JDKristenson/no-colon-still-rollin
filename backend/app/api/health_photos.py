"""Health photos API endpoints for medical tracking"""
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from typing import Optional, List
import sys
from pathlib import Path
from datetime import datetime
import shutil

sys.path.insert(0, str(Path(__file__).parent.parent / "core"))

from database import Database
from config import PROJECT_ROOT

router = APIRouter()

# Photos directory
PHOTOS_DIR = PROJECT_ROOT / "core" / "data" / "health_photos"
PHOTOS_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload")
async def upload_health_photo(
    file: UploadFile = File(...),
    user_id: int = Form(1),
    date: Optional[str] = Form(None),
    photo_type: str = Form("health"),
    notes: Optional[str] = Form("")
):
    """
    Upload a health photo for medical tracking

    Parameters:
    - file: Image file (JPEG, PNG)
    - user_id: User ID
    - date: Date of photo (ISO format), defaults to today
    - photo_type: Type of photo (default: "health")
    - notes: Optional notes about the photo
    """
    try:
        # Validate file type
        if not file.content_type or not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")

        # Generate unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        ext = Path(file.filename).suffix if file.filename else '.jpg'
        filename = f"user{user_id}_{timestamp}_{photo_type}{ext}"
        file_path = PHOTOS_DIR / filename

        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Add to database
        db = Database()
        photo_id = db.add_health_photo({
            'user_id': user_id,
            'date': date or datetime.now().isoformat(),
            'photo_type': photo_type,
            'filename': filename,
            'file_path': str(file_path),
            'notes': notes or ''
        })
        db.close()

        return {
            "message": "Photo uploaded successfully",
            "photo_id": photo_id,
            "filename": filename
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list")
def list_health_photos(user_id: int = 1, limit: int = 100):
    """Get list of health photos for a user"""
    try:
        db = Database()
        photos = db.get_health_photos(user_id, limit)
        db.close()

        # Return photo records with API URLs
        for photo in photos:
            photo['url'] = f"/api/health-photos/view/{photo['id']}"

        return photos

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/view/{photo_id}")
def view_health_photo(photo_id: int):
    """View a specific health photo"""
    try:
        db = Database()
        cursor = db.conn.cursor()
        cursor.execute("SELECT * FROM health_photos WHERE id = ?", (photo_id,))
        photo = cursor.fetchone()
        db.close()

        if not photo:
            raise HTTPException(status_code=404, detail="Photo not found")

        photo_dict = dict(photo)
        file_path = Path(photo_dict['file_path'])

        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Photo file not found")

        return FileResponse(
            file_path,
            media_type="image/jpeg",
            filename=photo_dict['filename']
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{photo_id}")
def delete_health_photo(photo_id: int):
    """Delete a health photo"""
    try:
        db = Database()
        cursor = db.conn.cursor()
        cursor.execute("SELECT file_path FROM health_photos WHERE id = ?", (photo_id,))
        result = cursor.fetchone()

        if not result:
            db.close()
            raise HTTPException(status_code=404, detail="Photo not found")

        file_path = Path(result[0])

        # Delete from database
        deleted = db.delete_health_photo(photo_id)
        db.close()

        # Delete physical file
        if file_path.exists():
            try:
                file_path.unlink()
            except:
                pass  # File already deleted or inaccessible

        if not deleted:
            raise HTTPException(status_code=404, detail="Photo not found")

        return {"message": "Photo deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
def get_health_photos_stats(user_id: int = 1):
    """Get statistics about health photos"""
    try:
        db = Database()
        cursor = db.conn.cursor()

        # Total photos
        cursor.execute("SELECT COUNT(*) FROM health_photos WHERE user_id = ?", (user_id,))
        total_photos = cursor.fetchone()[0]

        # Photos by type
        cursor.execute("""
            SELECT photo_type, COUNT(*) as count
            FROM health_photos
            WHERE user_id = ?
            GROUP BY photo_type
            ORDER BY count DESC
        """, (user_id,))
        by_type = [{"type": row[0], "count": row[1]} for row in cursor.fetchall()]

        # Most recent photo date
        cursor.execute("""
            SELECT date FROM health_photos
            WHERE user_id = ?
            ORDER BY date DESC
            LIMIT 1
        """, (user_id,))
        recent_result = cursor.fetchone()
        most_recent_date = recent_result[0] if recent_result else None

        db.close()

        return {
            "total_photos": total_photos,
            "by_type": by_type,
            "most_recent_date": most_recent_date
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{photo_id}/tags")
def update_photo_tags(photo_id: int, tags: List[str]):
    """Update tags for a health photo"""
    try:
        db = Database()
        success = db.update_health_photo_tags(photo_id, tags)
        db.close()

        if not success:
            raise HTTPException(status_code=404, detail="Photo not found")

        return {"message": "Tags updated successfully", "tags": tags}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{photo_id}/archive")
def archive_photo(photo_id: int, archived: bool = True):
    """Archive or unarchive a health photo"""
    try:
        db = Database()
        success = db.archive_health_photo(photo_id, archived)
        db.close()

        if not success:
            raise HTTPException(status_code=404, detail="Photo not found")

        action = "archived" if archived else "unarchived"
        return {"message": f"Photo {action} successfully"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list-filtered")
def list_health_photos_filtered(user_id: int = 1, archived: bool = False, limit: int = 100):
    """Get filtered list of health photos (active or archived)"""
    try:
        db = Database()
        photos = db.get_health_photos_filtered(user_id, archived, limit)
        db.close()

        # Return photo records with API URLs
        for photo in photos:
            photo['url'] = f"/api/health-photos/view/{photo['id']}"

        return photos

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
