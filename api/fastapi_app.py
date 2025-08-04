"""FastAPI endpoint exposing the tutorial agent."""

from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from agent import answer_question

app = FastAPI()


class Query(BaseModel):
    question: str
    tutorial_id: int | None = None
    video_id: str | None = None


@app.post("/ask")
def ask(query: Query) -> dict:
    answer = answer_question(
        question=query.question,
        tutorial_id=query.tutorial_id,
        video_id=query.video_id,
    )
    return {"answer": answer}
