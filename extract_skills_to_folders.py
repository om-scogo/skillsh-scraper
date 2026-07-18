#!/usr/bin/env python3
"""Extract skill folders from skills.json using skills-api.

For each matched skill, creates:
  - <source>/<skillId>/Skill.md
  - all other files returned by the API under <source>/<skillId>/
  - metadata.json (record of matched row and resolved source)

This script prefers the `owner` + `repo` from skills.json as the API key.
If those are missing, it attempts to infer `owner/repo` from `source`.
If still unresolved, it tries a search fallback.
"""

from __future__ import annotations

import argparse
import base64
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from typing import TypedDict


DEFAULT_API_BASE = "https://skills-api.development.scogo.ai/api/skills"
DEFAULT_INPUT = "/home/ubuntu/skillsh-scraper/data/skills.json"
DEFAULT_OUTPUT = "/home/ubuntu/skillsh-scraper/data/skills"


class ExtractError(RuntimeError):
    pass


class SkillsAPIError(TypedDict, total=False):
    error: str
    message: str
    documentation: str


def safe_component(name: str, fallback: str = "unknown") -> str:
    name = (name or "").strip()
    if not name:
        return fallback

    # Keep path components stable and deterministic; sanitize for filesystem safety
    name = re.sub(r"[\s/\\]+", "-", name)
    name = re.sub(r"[^A-Za-z0-9._-]", "-", name)
    name = re.sub(r"-+", "-", name).strip("-_.")
    return name or fallback


def decode_content(data: Dict[str, Any]) -> bytes:
    raw = data.get("content")
    if raw is None:
        return b""

    if not isinstance(raw, str):
        raw = str(raw)

    encoding = str(data.get("encoding") or "utf-8").lower()
    if encoding in {"base64", "utf-8"}:
        if encoding == "base64":
            return base64.b64decode(raw)
        return raw.encode("utf-8")

    # Unknown encodings from this API are unlikely; assume plain string.
    return raw.encode("utf-8")


def load_skills(path: Path) -> List[Dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, dict):
        if isinstance(payload.get("skills"), list):
            return payload["skills"]
    if isinstance(payload, list):
        return payload
    raise ExtractError("skills.json must contain a list or object with key 'skills'")


def build_headers() -> Dict[str, str]:
    return {
        "User-Agent": "skillsh-scraper/1.0",
        "Accept": "application/json",
    }


def fetch_json(url: str, headers: Dict[str, str], timeout: int = 30) -> Tuple[Optional[Dict[str, Any]], int, str]:
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            status = getattr(resp, "status", 200)
            if not raw.strip():
                return {}, status, ""
            return json.loads(raw), status, raw
    except urllib.error.HTTPError as exc:
        body = ""
        try:
            body = exc.read().decode("utf-8", errors="replace")
        except Exception:
            body = ""
        return None, getattr(exc, "code", 0), body
    except Exception:
        return None, 0, ""


def resolve_owner_repo(skill: Dict[str, Any]) -> Tuple[str, str]:
    owner = str(skill.get("owner") or "").strip()
    repo = str(skill.get("repo") or "").strip()

    if owner and repo:
        return owner, repo

    source = str(skill.get("source") or "").strip()
    if "/" in source:
        p, q = source.split("/", 1)
        if p and q:
            return p, q

    return "", ""


def normalize_api_base(api_base: str) -> str:
    return api_base.rstrip("/")


def find_skill_by_query(api_base: str, headers: Dict[str, str], skill: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    skill_id = str(skill.get("skillId") or "").strip()
    source = str(skill.get("source") or "").strip()

    if not skill_id:
        return None

    # Search endpoint (official endpoint supports `query` and optional `pageSize`).
    url = f"{api_base}?query={urllib.parse.quote(skill_id)}&pageSize=50"
    data, status, _ = fetch_json(url, headers)
    if status != 200 or not isinstance(data, dict):
        return None

    matches = data.get("skills") or []
    if not isinstance(matches, list):
        return None

    exact = [m for m in matches if str(m.get("skillId") or "") == skill_id]

    # If source is provided, require exact source match.
    # Do not silently switch to another source/repo when duplicates exist.
    if source:
        exact = [m for m in exact if str(m.get("source") or "") == source]

    if exact:
        return exact[0]
    return None


def fetch_files_payload(api_base: str, owner: str, repo: str, skill_id: str, headers: Dict[str, str]) -> Optional[Dict[str, Any]]:
    url = f"{api_base}/{urllib.parse.quote(owner)}/{urllib.parse.quote(repo)}/{urllib.parse.quote(skill_id)}/files"
    data, status, _ = fetch_json(url, headers)
    if status == 200 and isinstance(data, dict):
        return data
    return None


def fetch_content_payload(api_base: str, owner: str, repo: str, skill_id: str, headers: Dict[str, str]) -> Optional[Dict[str, Any]]:
    url = f"{api_base}/{urllib.parse.quote(owner)}/{urllib.parse.quote(repo)}/{urllib.parse.quote(skill_id)}/content"
    data, status, _ = fetch_json(url, headers)
    if status == 200 and isinstance(data, dict):
        return data
    return None


def write_file_bytes(target_root: Path, rel_path: str, content: bytes) -> None:
    dst = target_root / rel_path
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(content)


def extract_one(skill: Dict[str, Any], out_root: Path, api_base: str, headers: Dict[str, str], use_search_fallback: bool) -> Tuple[bool, str]:
    skill_id = str(skill.get("skillId") or skill.get("id") or "").strip()
    source = str(skill.get("source") or "").strip() or "unknown-source"

    owner, repo = resolve_owner_repo(skill)
    resolved_from = "skills.json"

    if (not owner or not repo) and use_search_fallback:
        found = find_skill_by_query(api_base, headers, skill)
        if found:
            owner, repo = resolve_owner_repo(found)
            source = str(found.get("source") or source).strip() or source
            skill_id = str(found.get("skillId") or skill_id).strip()
            resolved_from = "search-fallback"

    if not owner or not repo:
        return False, "missing owner/repo source mapping in skills.json"

    out_dir = out_root / safe_component(source) / safe_component(skill_id)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Always keep source context for traceability.
    (out_dir / "metadata.json").write_text(
        json.dumps(
            {
                "skillId": skill_id,
                "source": source,
                "owner": owner,
                "repo": repo,
                "resolved_from": resolved_from,
                "origin": skill,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    files_payload = fetch_files_payload(api_base, owner, repo, skill_id, headers)
    wrote = False

    if isinstance(files_payload, dict):
        files = files_payload.get("files")
        if isinstance(files, list) and files:
            for f in files:
                if not isinstance(f, dict):
                    continue
                rel = str(f.get("path") or "").strip()
                if not rel:
                    continue
                content = decode_content(f)
                write_file_bytes(out_dir, rel, content)
                wrote = True

                # Ensure canonical Skill.md exists at the expected location.
                if rel.lower() == "skill.md":
                    write_file_bytes(out_dir, "Skill.md", content)

            # If Skill.md was in a nested path, duplicate it to the canonical filename.
            skill_md_candidates = [
                p
                for p in [str(x.get("path") or "") for x in files if isinstance(x, dict)]
                if p and Path(p).name.lower() == "skill.md"
            ]
            if wrote and not (out_dir / "Skill.md").exists() and any(
                "skill.md" in p.lower() for p in skill_md_candidates
            ):
                # Copy first matched candidate
                for p in skill_md_candidates:
                    if "skill.md" in p.lower():
                        raw = (out_dir / p).read_bytes()
                        write_file_bytes(out_dir, "Skill.md", raw)
                        break

        if wrote:
            return True, f"{owner}/{repo}/{skill_id} (files:{len(files) if isinstance(files, list) else 0})"

    # Fallback to /content endpoint for legacy SKILL.md-only cases.
    content_payload = fetch_content_payload(api_base, owner, repo, skill_id, headers)
    if isinstance(content_payload, dict):
        raw = content_payload.get("raw")
        if isinstance(raw, str) and raw:
            rel = str(content_payload.get("path") or "SKILL.md").strip()
            if not rel:
                rel = "SKILL.md"
            write_file_bytes(out_dir, rel, raw.encode("utf-8"))
            write_file_bytes(out_dir, "Skill.md", raw.encode("utf-8"))
            return True, f"{owner}/{repo}/{skill_id} (content endpoint)"

    return False, f"No content endpoint data for {owner}/{repo}/{skill_id}"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Extract full skill folders from skills-api")
    p.add_argument("--input", default=DEFAULT_INPUT, help="Path to skills.json")
    p.add_argument("--output-dir", default=DEFAULT_OUTPUT, help="Destination root for extracted skills")
    p.add_argument("--api-base", default=DEFAULT_API_BASE, help="Skills API base URL")
    p.add_argument("--limit", type=int, default=None, help="Only extract first N matches after filtering")
    p.add_argument("--skill-id", help="Only extract a specific skillId")
    p.add_argument("--source", help="Only extract matching source")
    p.add_argument("--owner", help="Force owner override")
    p.add_argument("--repo", help="Force repo override")
    p.add_argument("--no-search-fallback", action="store_true", help="Disable query fallback")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    input_path = Path(args.input).expanduser()
    out_root = Path(args.output_dir).expanduser()
    out_root.mkdir(parents=True, exist_ok=True)

    skills = load_skills(input_path)

    headers = build_headers()
    api_base = normalize_api_base(args.api_base)

    matched: List[Dict[str, Any]] = []
    for s in skills:
        if not isinstance(s, dict):
            continue

        if args.skill_id and str(s.get("skillId") or s.get("id") or "") != args.skill_id:
            continue
        if args.source and str(s.get("source") or "") != args.source:
            continue
        matched.append(s)

    if not matched:
        raise ExtractError("No matching skill entries found in input")

    if args.limit is not None:
        matched = matched[: args.limit]

    total = len(matched)
    extracted = skipped = 0

    for idx, skill in enumerate(matched, start=1):
        # Optional explicit override; useful for edge rows like open.* sources
        if args.owner and args.repo:
            skill = dict(skill)
            skill["owner"] = args.owner
            skill["repo"] = args.repo

        ok, reason = extract_one(
            skill=skill,
            out_root=out_root,
            api_base=api_base,
            headers=headers,
            use_search_fallback=(not args.no_search_fallback),
        )
        if ok:
            extracted += 1
            status = "OK"
        else:
            skipped += 1
            status = "SKIP"
        print(f"[{idx}/{total}] {status} skillId={skill.get('skillId') or skill.get('id')} source={skill.get('source')} detail={reason}")

    print(f"[done] processed={total} extracted={extracted} skipped={skipped}")


if __name__ == "__main__":
    main()
