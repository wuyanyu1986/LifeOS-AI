#!/usr/bin/env python3
"""Create a WeChat Official Account draft without publishing it."""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import re
import ssl
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid
from dataclasses import dataclass
from pathlib import Path


STABLE_TOKEN_URL = "https://api.weixin.qq.com/cgi-bin/stable_token"
MATERIAL_URL = "https://api.weixin.qq.com/cgi-bin/material/add_material"
DRAFT_URL = "https://api.weixin.qq.com/cgi-bin/draft/add"


def tls_context() -> ssl.SSLContext:
    try:
        import certifi
    except ImportError:
        return ssl.create_default_context()
    return ssl.create_default_context(cafile=certifi.where())


class WeChatAPIError(RuntimeError):
    pass


@dataclass(frozen=True)
class Article:
    title: str
    digest: str
    html: str


def load_env_file(path: Path | None) -> None:
    if not path or not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip("'\""))


def required_credentials() -> tuple[str, str]:
    app_id = os.environ.get("WECHAT_MP_APP_ID", "").strip()
    app_secret = os.environ.get("WECHAT_MP_APP_SECRET", "").strip()
    if not app_id or not app_secret:
        raise WeChatAPIError(
            "Missing WECHAT_MP_APP_ID or WECHAT_MP_APP_SECRET in the local config."
        )
    return app_id, app_secret


def request_json(
    url: str, payload: dict | None = None, headers: dict[str, str] | None = None
) -> dict:
    data = None
    request_headers = dict(headers or {})
    if payload is not None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        request_headers.setdefault("Content-Type", "application/json; charset=utf-8")
    request = urllib.request.Request(url, data=data, headers=request_headers)
    try:
        with urllib.request.urlopen(
            request, timeout=30, context=tls_context()
        ) as response:
            result = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
        raise WeChatAPIError(f"WeChat request failed: {error}") from error
    if result.get("errcode") not in (None, 0):
        raise WeChatAPIError(
            f"WeChat API error {result.get('errcode')}: {result.get('errmsg', '')}"
        )
    return result


def get_access_token(app_id: str, app_secret: str) -> str:
    result = request_json(
        STABLE_TOKEN_URL,
        {
            "grant_type": "client_credential",
            "appid": app_id,
            "secret": app_secret,
            "force_refresh": False,
        },
    )
    token = result.get("access_token")
    if not token:
        raise WeChatAPIError("WeChat did not return an access_token.")
    return str(token)


def extract_article(markdown_path: Path) -> Article:
    source = markdown_path.read_text(encoding="utf-8")
    source = re.sub(r"^>\s*[🟡✅⚠️].*?\n+", "", source, count=1)
    title_match = re.search(r"^#\s+(.+)$", source, flags=re.MULTILINE)
    if not title_match:
        raise WeChatAPIError("The article must contain one H1 title.")
    title = title_match.group(1).strip()
    body = source[title_match.end() :].lstrip()
    digest_match = re.match(r">\s*(.+?)(?:\n\n|\Z)", body, flags=re.DOTALL)
    digest = ""
    if digest_match:
        digest = " ".join(
            line.lstrip("> ").strip()
            for line in digest_match.group(1).splitlines()
        )
        body = body[digest_match.end() :]
    body = re.split(r"\n---\n|\n##\s+备选标题\s*\n", body, maxsplit=1)[0].strip()
    try:
        import markdown as markdown_module
    except ImportError as error:
        raise WeChatAPIError("Python package 'Markdown' is required.") from error
    rendered = markdown_module.markdown(body, extensions=["extra", "sane_lists"])
    html = (
        '<section style="font-size:16px;line-height:1.8;color:#242424;">'
        + rendered
        + "</section>"
    )
    validate_article(title, digest, html)
    return Article(title=title, digest=digest, html=html)


def validate_article(title: str, digest: str, content: str) -> None:
    if len(title) > 32:
        raise WeChatAPIError("WeChat title must not exceed 32 characters.")
    if len(digest) > 120:
        raise WeChatAPIError("WeChat digest must not exceed 120 characters.")
    if len(content) >= 20_000 or len(content.encode("utf-8")) >= 1_000_000:
        raise WeChatAPIError("WeChat article content exceeds the API limit.")


def image_dimensions(path: Path) -> tuple[int, int]:
    result = subprocess.run(
        ["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(path)],
        check=True,
        capture_output=True,
        text=True,
    )
    width = re.search(r"pixelWidth:\s*(\d+)", result.stdout)
    height = re.search(r"pixelHeight:\s*(\d+)", result.stdout)
    if not width or not height:
        raise WeChatAPIError("Unable to read cover dimensions.")
    return int(width.group(1)), int(height.group(1))


def validate_cover(path: Path) -> None:
    if path.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
        raise WeChatAPIError("Cover must be a JPG or PNG image.")
    if path.stat().st_size > 10 * 1024 * 1024:
        raise WeChatAPIError("Cover exceeds the 10 MB material limit.")
    if image_dimensions(path) != (900, 900):
        raise WeChatAPIError("Cover master must be exactly 900x900 pixels.")


def upload_permanent_cover(access_token: str, cover_path: Path) -> str:
    boundary = f"----LifeOS{uuid.uuid4().hex}"
    mime = mimetypes.guess_type(cover_path.name)[0] or "application/octet-stream"
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="media"; filename="{cover_path.name}"\r\n'
        f"Content-Type: {mime}\r\n\r\n"
    ).encode("utf-8") + cover_path.read_bytes() + f"\r\n--{boundary}--\r\n".encode(
        "utf-8"
    )
    query = urllib.parse.urlencode({"access_token": access_token, "type": "image"})
    request = urllib.request.Request(
        f"{MATERIAL_URL}?{query}",
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    try:
        with urllib.request.urlopen(
            request, timeout=60, context=tls_context()
        ) as response:
            result = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
        raise WeChatAPIError(f"Cover upload failed: {error}") from error
    if result.get("errcode") not in (None, 0):
        raise WeChatAPIError(
            f"WeChat API error {result.get('errcode')}: {result.get('errmsg', '')}"
        )
    media_id = result.get("media_id")
    if not media_id:
        raise WeChatAPIError("WeChat did not return a permanent cover media_id.")
    return str(media_id)


def build_draft_payload(
    article: Article, author: str, cover_media_id: str
) -> dict:
    if len(author) > 16:
        raise WeChatAPIError("WeChat author must not exceed 16 characters.")
    return {
        "articles": [
            {
                "article_type": "news",
                "title": article.title,
                "author": author,
                "digest": article.digest,
                "content": article.html,
                "thumb_media_id": cover_media_id,
                "need_open_comment": 0,
                "only_fans_can_comment": 0,
                "cover_info": {
                    "crop_percent_list": [
                        {
                            "ratio": "2.35_1",
                            "x1": "0",
                            "y1": "0.287234",
                            "x2": "1",
                            "y2": "0.712766",
                        },
                        {
                            "ratio": "1_1",
                            "x1": "0",
                            "y1": "0",
                            "x2": "1",
                            "y2": "1",
                        },
                    ]
                },
            }
        ]
    }


def create_draft(access_token: str, payload: dict) -> str:
    query = urllib.parse.urlencode({"access_token": access_token})
    result = request_json(f"{DRAFT_URL}?{query}", payload)
    media_id = result.get("media_id")
    if not media_id:
        raise WeChatAPIError("WeChat did not return a draft media_id.")
    return str(media_id)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--article", type=Path, required=True)
    parser.add_argument("--cover-square", type=Path, required=True)
    parser.add_argument("--env-file", type=Path)
    parser.add_argument("--author", default="")
    parser.add_argument("--dry-run", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    load_env_file(args.env_file)
    article = extract_article(args.article)
    validate_cover(args.cover_square)
    author = args.author or os.environ.get("WECHAT_MP_AUTHOR", "")
    if args.dry_run:
        payload = build_draft_payload(article, author, "DRY_RUN_MEDIA_ID")
        print(
            json.dumps(
                {
                    "ok": True,
                    "dry_run": True,
                    "title": article.title,
                    "digest": article.digest,
                    "content_chars": len(article.html),
                    "cover": str(args.cover_square),
                    "payload": payload,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0
    app_id, app_secret = required_credentials()
    access_token = get_access_token(app_id, app_secret)
    cover_media_id = upload_permanent_cover(access_token, args.cover_square)
    payload = build_draft_payload(article, author, cover_media_id)
    draft_media_id = create_draft(access_token, payload)
    print(
        json.dumps(
            {
                "ok": True,
                "cover_media_id": cover_media_id,
                "draft_media_id": draft_media_id,
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (WeChatAPIError, OSError, subprocess.CalledProcessError) as error:
        print(json.dumps({"ok": False, "error": str(error)}, ensure_ascii=False))
        raise SystemExit(1)
