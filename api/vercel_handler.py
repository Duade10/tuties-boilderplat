"""Vercel serverless function entrypoint."""

from __future__ import annotations

import json
from typing import Any

from agent import answer_question


def handler(request: Any) -> Any:
    if hasattr(request, "json"):
        body = request.json()
    else:
        body = json.loads(getattr(request, "body", "{}"))
    question = body.get("question", "")
    tutorial_id = body.get("tutorial_id")
    video_id = body.get("video_id")
    answer = answer_question(question, tutorial_id, video_id)
    return {"statusCode": 200, "body": json.dumps({"answer": answer})}
