"""Topic slug sanitization for workspace directory names."""

from __future__ import annotations

import re
import unicodedata


def sanitize_slug(topic: str, max_length: int = 60) -> str:
    slug = topic.lower()
    slug = unicodedata.normalize("NFKD", slug)
    slug = re.sub(r"[^\x00-\x7f]", "-", slug)
    slug = re.sub(r"[/\\\.~:;!@#$%^&*()+=\[\]{}<>|`'\",?]", "-", slug)
    slug = re.sub(r"\s+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    slug = slug.strip("-")
    if len(slug) > max_length:
        slug = slug[:max_length].rstrip("-")
    return slug or "untitled"
