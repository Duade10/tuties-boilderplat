"""HTTP handler compatible with n8n's HTTP Request node."""

from __future__ import annotations

import json
from typing import Any, Dict

from agent import answer_question


def handler(event: Dict[str, Any], context: Dict[str, Any] | None = None) -> Dict[str, Any]:
    body = json.loads(event.get("body", "{}"))
    question = body.get("question", "")
    tutorial_id = body.get("tutorial_id")
    video_id = body.get("video_id")
    answer = answer_question(question, tutorial_id, video_id)
    return {"statusCode": 200, "body": json.dumps({"answer": answer})}
