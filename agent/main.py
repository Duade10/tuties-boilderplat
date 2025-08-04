"""Core agent logic for building context and answering questions."""

from __future__ import annotations

from .clients import MuxClient, OpenAIClient, StrapiClient, SupabaseClient

strapi_client = StrapiClient()
mux_client = MuxClient()
supabase_client = SupabaseClient()
openai_client = OpenAIClient()


def build_context(tutorial_id: int | None, video_id: str | None) -> str:
    """Collect metadata, transcripts and comments into a context string."""
    parts: list[str] = []
    metadata: dict = {}
    comments: list[str] = []
    transcript = ""

    if tutorial_id is not None:
        metadata = strapi_client.get_tutorial(tutorial_id)
        comments = supabase_client.get_comments(tutorial_id)
    if video_id:
        transcript = mux_client.get_transcript(video_id)

    if metadata:
        parts.append(f"Title: {metadata.get('title', '')}")
        if metadata.get("tags"):
            parts.append("Tags: " + ", ".join(metadata["tags"]))
        if metadata.get("description"):
            parts.append("Description: " + metadata["description"])
    if transcript:
        parts.append("Transcript:\n" + transcript)
    if comments:
        parts.append("Comments:\n" + "\n".join(comments))
    return "\n".join(parts)


def answer_question(question: str, tutorial_id: int | None = None, video_id: str | None = None, log: bool = True) -> str:
    """Return an OpenAI-generated answer for the given question."""
    system_prompt = build_context(tutorial_id, video_id)
    answer = openai_client.ask(system_prompt, question)
    if log and tutorial_id is not None:
        supabase_client.log_interaction({
            "tutorial_id": tutorial_id,
            "question": question,
            "answer": answer,
        })
    return answer
