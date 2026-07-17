#!/usr/bin/env python3
"""Scrape the official skills.sh v1 API and write registry JSON.

Usage:
  python scrape_skills_official.py --token "YOUR_TOKEN"

Output format matches:
  src/registry/scraped-skills.json in @scogo/skills-api.
"""

from __future__ import annotations
import os
import argparse
import json
import math
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from dotenv import load_dotenv


load_dotenv()

DEFAULT_RATE_DELAY_SECONDS = 0.12  # Slightly below 600/min = 10 req/s
DEFAULT_PER_PAGE = 500
MAX_RETRIES = 5
TIMEOUT_SECONDS = 30


@dataclass
class RateLimitState:
    limit: Optional[int] = None
    remaining: Optional[int] = None
    reset_seconds: Optional[int] = None


def parse_int(value: Optional[str]) -> Optional[int]:
    if value is None:
        return None
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return None


def extract_rate_limit(headers: Any) -> RateLimitState:
    return RateLimitState(
        limit=parse_int(headers.get("X-RateLimit-Limit")),
        remaining=parse_int(headers.get("X-RateLimit-Remaining")),
        reset_seconds=parse_int(headers.get("X-RateLimit-Reset")),
    )


def resolve_output_path(custom_path: Optional[str]) -> Path:
    if custom_path:
        return Path(custom_path).expanduser().resolve()

    # Default to a local folder inside this project: ./scraped-data/scraped-skills.json
    root = Path(__file__).resolve().parent
    default_target = root / "scraped-data" / "scraped-skills.json"
    return default_target


def display_name_from_skill_id(skill_id: str) -> str:
    return (" ".join(part.capitalize() for part in skill_id.replace("_", "-").split("-") if part)).strip()


def normalize_skill(item: Dict[str, Any]) -> Dict[str, Any]:
    source = item.get("source")
    skill_id = item.get("slug") or item.get("skillId")

    # Some responses may only expose `id` (source/slug)
    if not skill_id:
        raw_id = item.get("id", "")
        if isinstance(raw_id, str) and "/" in raw_id:
            source = source or raw_id.rsplit("/", 1)[0]
            skill_id = raw_id.rsplit("/", 1)[1]
        else:
            skill_id = str(raw_id or "")

    source = source or ""
    owner, repo = ("", "")
    if "/" in source:
        parts = source.split("/", 1)
        owner, repo = parts[0], parts[1]

    installs = item.get("installs", 0)
    try:
        installs = int(installs)
    except (TypeError, ValueError):
        installs = 0

    name = str(item.get("name") or skill_id)
    raw_display_name = item.get("displayName")
    display_name = str(raw_display_name).strip() if raw_display_name else display_name_from_skill_id(str(skill_id))

    return {
        "source": str(source),
        "skillId": str(skill_id),
        "name": name,
        "installs": installs,
        "owner": str(owner),
        "repo": str(repo),
        "githubUrl": f"https://github.com/{source}" if source else "",
        "displayName": display_name,
    }


def normalize_list_response(payload: Any) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """Return (items, meta)."""
    if isinstance(payload, list):
        return payload, {}

    if not isinstance(payload, dict):
        raise ValueError("Unexpected response payload type from skills.sh")

    # Common shapes:
    # {skills: [...], total: N, hasMore: true}
    # {data: [...], page: ...}
    # {data: {skills: [...], total: N}}
    if isinstance(payload.get("skills"), list):
        return payload.get("skills", []), payload

    if isinstance(payload.get("data"), list):
        return payload.get("data", []), payload

    data = payload.get("data")
    if isinstance(data, dict) and isinstance(data.get("skills"), list):
        return data.get("skills", []), {**payload, **data}

    raise ValueError("Could not find skills array in response JSON")


def _get_meta_value(meta: Dict[str, Any], keys: Tuple[str, ...]) -> Optional[Any]:
    for key in keys:
        if key in meta:
            return meta[key]
    return None


def done_by_total_count(page_items: int, page: int, per_page: int, meta: Dict[str, Any], seen: int) -> bool:
    # explicit total count fields
    total = _get_meta_value(meta, ("total", "totalCount", "total_count", "totalItems", "total_items"))
    if isinstance(total, (int, float)):
        return seen >= int(total)

    # explicit pagination fields
    total_pages = _get_meta_value(meta, ("totalPages", "total_pages", "pages", "pageCount"))
    if isinstance(total_pages, (int, float)) and int(total_pages) > 0:
        return page >= int(total_pages) - 1

    # fallback for old-style endpoint and unknown shapes
    has_more = _get_meta_value(meta, ("hasMore", "has_more"))
    if isinstance(has_more, bool):
        return not has_more

    # fallback: short last page
    if 0 < page_items < per_page:
        return True

    if page_items == 0:
        return True

    return False


def done_by_has_more(payload_meta: Dict[str, Any], page_items: int, per_page: int) -> bool:
    has_more = payload_meta.get("hasMore") if isinstance(payload_meta, dict) else None
    if isinstance(has_more, bool):
        return not has_more

    total = payload_meta.get("total") if isinstance(payload_meta, dict) else None
    if isinstance(total, (int, float)) and total < 0:
        return False

    if page_items == 0 or page_items < per_page:
        return True

    return False


def should_wait_rate_limit(rl: RateLimitState) -> Optional[float]:
    # If remaining is low and reset window is near, wait until reset.
    if rl.remaining is not None and rl.remaining <= 2 and rl.reset_seconds is not None:
        # reset is seconds-until-window-reset, from API docs.
        return max(rl.reset_seconds + 0.2, 0.2)
    return None


def request_page(
    token: str,
    api_base: str,
    view: str,
    page: int,
    per_page: int,
) -> Tuple[List[Dict[str, Any]], Dict[str, Any], RateLimitState]:
    params = {
        "view": view,
        "page": str(page),
        "per_page": str(per_page),
    }
    url = f"{api_base}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "x-vercel-oidc-token": token,
            "User-Agent": "skillsh-scraper/1.0 (+https://github.com/om)",
            "Accept": "application/json",
        },
        method="GET",
    )

    attempt = 0
    while True:
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
                body = resp.read().decode("utf-8")
                payload = json.loads(body)
                rl = extract_rate_limit(resp.headers)
                items, meta = normalize_list_response(payload)
                # Keep meta fallback fields if page-level response includes them.
                if not isinstance(meta, dict):
                    meta = {}
                meta.setdefault("_headers", {})
                meta["_headers"].update(dict(resp.headers))
                return items, meta, rl

        except urllib.error.HTTPError as exc:
            status = getattr(exc, "code", None)
            body = exc.read().decode("utf-8", errors="ignore")
            if status in (401, 403):
                raise RuntimeError(
                    f"Authentication failed ({status}). Provide a valid Vercel OIDC token."
                ) from None

            if status == 429:
                retry_after = parse_int(exc.headers.get("Retry-After"))
                if attempt >= MAX_RETRIES:
                    raise RuntimeError("Hit 429 Too Many Requests repeatedly. Aborting.") from None

                delay = float(retry_after or 2)
                print(f"[rate limit] 429 received; retrying in {delay}s", flush=True)
                time.sleep(delay)
                attempt += 1
                continue

            # Retry transient 5xx for a little while
            if status and 500 <= status < 600 and attempt < MAX_RETRIES:
                delay = (2**attempt) * 1.0
                print(f"[retry] HTTP {status} on page {page}; retrying in {delay}s", flush=True)
                time.sleep(delay)
                attempt += 1
                continue

            raise RuntimeError(f"HTTP {status} while fetching page {page}: {body}") from None

        except urllib.error.URLError as exc:
            if attempt >= MAX_RETRIES:
                raise RuntimeError(f"Network error while fetching page {page}: {exc}") from exc
            delay = (2**attempt) * 0.8
            print(f"[retry] network error on page {page}; retrying in {delay}s", flush=True)
            time.sleep(delay)
            attempt += 1


def scrape_all(token: str, api_base: str, view: str = "all-time", per_page: int = DEFAULT_PER_PAGE, max_pages: Optional[int] = None) -> List[Dict[str, Any]]:
    page = 0
    all_skills: List[Dict[str, Any]] = []
    seen_ids = set()
    request_count = 0

    while True:
        if max_pages is not None and page >= max_pages:
            break

        items, meta, rl = request_page(token=token, api_base=api_base, view=view, page=page, per_page=per_page)
        request_count += 1
        request_interval = DEFAULT_RATE_DELAY_SECONDS

        # rate-limit header check (proactive)
        wait_for_reset = should_wait_rate_limit(rl)
        if wait_for_reset and wait_for_reset > 0.0:
            print(f"[rate limit] remaining={rl.remaining}, reset={rl.reset_seconds}s; sleeping for reset window")
            time.sleep(wait_for_reset)

        normalized_items = []
        for raw in items:
            try:
                mapped = normalize_skill(raw)
            except Exception:
                # Keep scraper resilient; skip malformed entries.
                continue

            # stable dedupe by source + skillId/id
            item_id = f"{mapped['source']}/{mapped['skillId']}" if mapped.get("source") else mapped.get("skillId", "")
            if item_id in seen_ids:
                continue
            seen_ids.add(item_id)
            normalized_items.append(mapped)

        all_skills.extend(normalized_items)

        if request_count % 10 == 0:
            print(f"[{request_count}] fetched page {page} -> {len(normalized_items)} skills; total={len(all_skills)}")

        if done_by_total_count(len(items), page, per_page, meta, len(all_skills)):
            break

        # fallback for old endpoints and unknown metadata shapes
        if done_by_has_more(meta, len(items), per_page):
            break

        page += 1

        # Respect token bucket from docs: 600 requests/min. Stay comfortably under with tiny delay.
        time.sleep(request_interval)

    return all_skills


def summarize_and_write(skills: List[Dict[str, Any]], output_path: Path) -> Dict[str, Any]:
    total_skills = len(skills)
    total_sources = len({s["source"] for s in skills if s.get("source")})
    total_owners = len({s["owner"] for s in skills if s.get("owner")})

    payload = {
        "scrapedAt": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "totalSkills": total_skills,
        "totalSources": total_sources,
        "totalOwners": total_owners,
        "skills": skills,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = output_path.with_suffix(output_path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    tmp.replace(output_path)
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scrape skills.sh with official API and export registry JSON")
    parser.add_argument("--token", help="Vercel OIDC token for skills.sh API")
    parser.add_argument("--output", help="Output file path (default: ./scraped-data/scraped-skills.json)")
    parser.add_argument("--view", default="all-time", choices=["all-time", "trending", "hot"], help="Leaderboard view")
    parser.add_argument("--per-page", type=int, default=DEFAULT_PER_PAGE, help="Items per page (1-500)")
    parser.add_argument("--max-pages", type=int, default=None, help="Optional stop after N pages (debug helper)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    api_base = os.getenv("VERCEL_API_BASE")
    print(f"api_base: {api_base}")
    token = args.token or os.getenv("VERCEL_OIDC_TOKEN")
    print(token)

    if not token:
        raise RuntimeError("Provide token with --token or env VERCEL_OIDC_TOKEN")

    if not api_base:
        raise RuntimeError("Set VERCEL_API_BASE in .env or environment")

    if not (1 <= args.per_page <= 500):
        raise RuntimeError("--per-page must be between 1 and 500")

    output = resolve_output_path(args.output)
    print(f"[start] output: {output}")
    print(f"[start] outputting leaderboard view={args.view}, per_page={args.per_page}")

    skills = scrape_all(token=token, api_base=api_base, view=args.view, per_page=args.per_page, max_pages=args.max_pages)
    if not skills:
        raise RuntimeError("No skills scraped. Check token and API access.")

    payload = summarize_and_write(skills, output)

    print(f"[done] totalSkills: {payload['totalSkills']}")
    print(f"[done] totalSources: {payload['totalSources']}")
    print(f"[done] totalOwners: {payload['totalOwners']}")
    print(f"[done] saved: {output}")


if __name__ == "__main__":
    import os

    main()
