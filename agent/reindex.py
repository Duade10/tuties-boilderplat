"""Utilities for reindexing tutorials when content changes."""

from __future__ import annotations

from .clients import MuxClient, StrapiClient, SupabaseClient

strapi_client = StrapiClient()
mux_client = MuxClient()
supabase_client = SupabaseClient()


def reindex_tutorial(tutorial_id: int, video_id: str | None = None) -> dict:
    """Refresh metadata and transcript for a tutorial in Supabase index."""
    metadata = strapi_client.get_tutorial(tutorial_id)
    if video_id is None:
        video_id = metadata.get("video_id")
    transcript = mux_client.get_transcript(video_id) if video_id else ""
    supabase_client.upsert_index(tutorial_id, metadata, transcript)
    return {
        "tutorial_id": tutorial_id,
        "metadata": metadata,
        "transcript": transcript,
    }
