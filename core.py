from __future__ import annotations
import re
from typing import Callable, Optional
from openai import OpenAI
from .config import get_api_key, get_model, get_max_chunk_chars

class TranslationError(RuntimeError):
    pass

def split_text(text: str, max_chars: int) -> list[str]:
    """Split long text at paragraph/sentence boundaries without dropping text."""
    text = text.strip()
    if not text:
        return []
    if len(text) <= max_chars:
        return [text]

    paragraphs = re.split(r"(\\n\\s*\\n)", text)
    units: list[str] = []
    buffer = ""
    for part in paragraphs:
        candidate = buffer + part
        if len(candidate) <= max_chars:
            buffer = candidate
            continue
        if buffer:
            units.append(buffer)
            buffer = ""
        if len(part) <= max_chars:
            buffer = part
            continue
        sentences = re.split(r"(?<=[.!?。！？])\\s+", part)
        for sentence in sentences:
            if len(sentence) > max_chars:
                for start in range(0, len(sentence), max_chars):
                    units.append(sentence[start:start + max_chars])
            elif buffer and len(buffer) + len(sentence) <= max_chars:
                buffer += sentence
            else:
                if buffer:
                    units.append(buffer)
                buffer = sentence
    if buffer:
        units.append(buffer)
    return [u for u in units if u]

class Translator:
    def __init__(self, model: Optional[str] = None):
        self.model = model or get_model()

    def _client(self):
        key = get_api_key()
        if not key:
            raise TranslationError("Chưa có OPENAI_API_KEY. Hãy điền API key trong file .env.")
        return OpenAI(api_key=key)

    @staticmethod
    def _instructions(mode: str) -> str:
        if mode == "en_vi":
            return ("Translate naturally between English and Vietnamese. Detect the source language "
                    "automatically and translate into the other language. Preserve meaning, tone, "
                    "formatting, names, numbers, and technical terms. Return only the translation.")
        if mode == "zh_vi":
            return ("Translate the Chinese input into natural Vietnamese. Preserve meaning, tone, "
                    "formatting, names, numbers, and technical terms. Return only the Vietnamese translation.")
        raise TranslationError("Chế độ dịch không hợp lệ.")

    def translate(self, text: str, mode: str = "en_vi",
                  progress: Optional[Callable[[int, int], None]] = None) -> str:
        if not text or not text.strip():
            raise TranslationError("Vui lòng nhập nội dung cần dịch.")
        chunks = split_text(text, get_max_chunk_chars())
        client = self._client()
        results = []
        for index, chunk in enumerate(chunks, start=1):
            try:
                response = client.responses.create(
                    model=self.model,
                    instructions=self._instructions(mode),
                    input=chunk,
                )
                translated = (response.output_text or "").strip()
                if not translated:
                    raise TranslationError("API trả về kết quả trống.")
                results.append(translated)
                if progress:
                    progress(index, len(chunks))
            except TranslationError:
                raise
            except Exception as exc:
                raise TranslationError(f"Lỗi khi gọi OpenAI API (đoạn {index}/{len(chunks)}): {exc}") from exc
        return "\\n\\n".join(results)
