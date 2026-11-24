"""What the generator scripts share: reading the spec, and naming things after it."""

from __future__ import annotations

import argparse
import json
import os
import re
import urllib.request
from dataclasses import dataclass, field
from typing import Any

PYTHON_TYPES = {"string": "str", "integer": "int", "number": "float", "boolean": "bool"}


def load() -> dict[str, Any]:
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", default=os.environ.get("SPEC", "https://api.socialapi.sh/openapi.json"))
    source = parser.parse_args().spec
    if re.match(r"^https?://", source):
        # Cloudflare refuses urllib's own User-Agent ("Python-urllib/3.x") with a 403.
        request = urllib.request.Request(source, headers={"User-Agent": "socialapi-python-generator"})
        with urllib.request.urlopen(request) as response:  # noqa: S310 - our own spec
            return json.load(response)
    with open(source, encoding="utf-8") as file:
        return json.load(file)


def snake(name: str) -> str:
    """`secUid` → `sec_uid`, `tiktokPostCommentReplies` → `tiktok_post_comment_replies`."""
    return re.sub(r"(?<=[a-z0-9])([A-Z])", r"_\1", name).lower()


def attribute(tag: str) -> str:
    """The client's attribute for a tag: `TikTok` → `tiktok`."""
    return re.sub(r"[^a-z0-9]", "", tag.lower())


def api_class(tag: str) -> str:
    """The generator's class for a tag: `TikTok` → `TikTokApi`."""
    return re.sub(r"[^A-Za-z0-9]", "", tag) + "Api"


def api_module(tag: str) -> str:
    """The generator's module for a tag: `TikTok` → `tik_tok_api`."""
    return snake(re.sub(r"[^A-Za-z0-9]", "", tag)) + "_api"


def model_class(ref: str) -> str:
    """`#/components/schemas/Item_TikTokProfile` → `ItemTikTokProfile`."""
    return re.sub(r"[^A-Za-z0-9]", "", ref.rsplit("/", 1)[-1])


@dataclass
class Param:
    name: str
    python: str
    type: str
    required: bool
    description: str


@dataclass
class Endpoint:
    path: str
    tag: str
    operation_id: str
    summary: str
    #: The client's method (`profile_posts`).
    method: str
    #: The generated API class's method (`tiktok_profile_posts`).
    generated: str
    returns: str | None
    params: list[Param] = field(default_factory=list)


def endpoints(spec: dict[str, Any]) -> list[Endpoint]:
    out = []
    for path, item in spec.get("paths", {}).items():
        operation = item.get("get")
        if not operation or not operation.get("operationId") or not operation.get("tags"):
            continue
        tag = operation["tags"][0]
        prefix = attribute(tag)
        operation_id = operation["operationId"]
        method = snake(operation_id)
        if method.startswith(prefix + "_"):
            method = method[len(prefix) + 1 :]
        schema = (
            operation.get("responses", {}).get("200", {}).get("content", {}).get("application/json", {}).get("schema", {})
        )
        params = []
        for parameter in operation.get("parameters", []):
            if parameter.get("in") != "query":
                continue
            kind = parameter.get("schema", {}).get("type", "string")
            if isinstance(kind, list):
                kind = next((k for k in kind if k != "null"), "string")
            params.append(
                Param(
                    name=parameter["name"],
                    python=snake(parameter["name"]),
                    type=PYTHON_TYPES.get(kind, "str"),
                    required=bool(parameter.get("required")),
                    description=" ".join(parameter.get("description", "").split()),
                )
            )
        out.append(
            Endpoint(
                path=path,
                tag=tag,
                operation_id=operation_id,
                summary=" ".join((operation.get("summary") or "").split()),
                method=method,
                generated=snake(operation_id),
                returns=model_class(schema["$ref"]) if "$ref" in schema else None,
                params=params,
            )
        )
    return out


def tags_in_order(items: list[Endpoint]) -> list[str]:
    """Platforms alphabetically, the account last."""
    tags = sorted({e.tag for e in items})
    return [t for t in tags if t != "Account"] + [t for t in tags if t == "Account"]
