"""API client implementations for external services."""

from __future__ import annotations

import json
from typing import List, Optional

import requests

try:
    import openai
except Exception:  # pragma: no cover - openai may not be installed
    openai = None

from .config import settings


class StrapiClient:
    """Fetch tutorial metadata from a Strapi CMS instance."""

    def __init__(self, base_url: str | None = None, token: str | None = None) -> None:
        self.base_url = (base_url or settings.strapi_url).rstrip("/")
        self.token = token or settings.strapi_token

    def get_tutorial(self, tutorial_id: int) -> dict:
        url = f"{self.base_url}/api/tutorials/{tutorial_id}?populate=*"
        headers: dict[str, str] = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json().get("data", {})
        attributes = data.get("attributes", {})
        tags = [t.get("name", "") for t in attributes.get("tags", {}).get("data", [])]
        return {
            "title": attributes.get("title", ""),
            "tags": tags,
            "description": attributes.get("description", ""),
        }


class MuxClient:
    """Retrieve video transcripts from Mux."""

    def __init__(self, token: str | None = None) -> None:
        self.token = token or settings.mux_token

    def get_transcript(self, video_id: str) -> str:
        url = f"https://stream.mux.com/{video_id}/text.vtt"
        headers: dict[str, str] = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text


class SupabaseClient:
    """Minimal Supabase client using RESTful endpoints."""

    def __init__(self, url: str | None = None, key: str | None = None) -> None:
        self.url = url or settings.supabase_url
        self.key = key or settings.supabase_key

    def _headers(self) -> dict[str, str]:
        return {
            "apikey": self.key or "",
            "Authorization": f"Bearer {self.key}" if self.key else "",
            "Content-Type": "application/json",
        }

    def get_comments(self, tutorial_id: int) -> List[str]:
        if not self.url or not self.key:
            return []
        params = {"tutorial_id": f"eq.{tutorial_id}", "select": "content"}
        response = requests.get(f"{self.url}/rest/v1/comments", params=params, headers=self._headers(), timeout=10)
        response.raise_for_status()
        return [c.get("content", "") for c in response.json()]

    def log_interaction(self, payload: dict) -> None:
        if not self.url or not self.key:
            return
        requests.post(
            f"{self.url}/rest/v1/interactions",
            headers=self._headers(),
            data=json.dumps(payload),
            timeout=10,
        ).raise_for_status()

    def upsert_index(self, tutorial_id: int, metadata: dict, transcript: str) -> None:
        if not self.url or not self.key:
            return
        payload = {
            "tutorial_id": tutorial_id,
            "title": metadata.get("title", ""),
            "tags": metadata.get("tags", []),
            "description": metadata.get("description", ""),
            "transcript": transcript,
        }
        requests.post(
            f"{self.url}/rest/v1/tutorial_index",
            headers=self._headers(),
            data=json.dumps(payload),
            timeout=10,
        ).raise_for_status()


class OpenAIClient:
    """Wrapper around the OpenAI Chat Completions API."""

    def __init__(self, api_key: str | None = None, model: str = "gpt-4o") -> None:
        self.api_key = api_key or settings.openai_api_key
        self.model = model

    def ask(self, system_prompt: str, question: str) -> str:
        if openai is None:
            raise RuntimeError("openai package is not installed")
        openai.api_key = self.api_key
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question},
            ],
        )
        return response.choices[0].message["content"]
