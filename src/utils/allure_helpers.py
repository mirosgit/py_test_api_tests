import json
from typing import Any, Mapping, Optional
import allure


def attach_json(title: str, data: Any) -> None:
    try:
        payload = json.dumps(data, indent=2, ensure_ascii=False)
    except Exception:
        payload = str(data)
    allure.attach(payload, name=title, attachment_type=allure.attachment_type.JSON)


def attach_text(title: str, text: str) -> None:
    allure.attach(text, name=title, attachment_type=allure.attachment_type.TEXT)


def as_curl(method: str, url: str, headers: Optional[Mapping[str, str]] = None, body: Optional[str] = None) -> str:
    parts = [f"curl -X {method.upper()} '{url}'"]
    for k, v in (headers or {}).items():
        parts.append(f"-H '{k}: {v}'")
    if body:
        parts.append(f"--data-raw '{body}'")
    return " \\\n  ".join(parts)
