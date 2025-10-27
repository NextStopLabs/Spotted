from django import template
import os

register = template.Library()

IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
VIDEO_EXTS = {'.mp4', '.mov', '.avi', '.webm', '.mkv'}
AUDIO_EXTS = {'.mp3', '.wav', '.ogg', '.m4a'}

@register.filter
def file_type(filename):
    """
    Returns 'image', 'video', 'audio', or 'file' based on file extension.
    """
    ext = os.path.splitext(filename)[1].lower()
    if ext in IMAGE_EXTS:
        return 'image'
    elif ext in VIDEO_EXTS:
        return 'video'
    elif ext in AUDIO_EXTS:
        return 'audio'
    return 'file'


@register.filter
def hashtags(value):
    """
    Converts a comma-separated tag list into spaced hashtags.
    Example:
        "Crewe, Stafford, RR" → "#Crewe #Stafford #RR"
    """
    if not value:
        return ""
    tags = [tag.strip().replace(" ", "") for tag in value.split(",") if tag.strip()]
    return " ".join(f"#{tag}" for tag in tags)