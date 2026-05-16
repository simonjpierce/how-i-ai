#!/usr/bin/env python3
"""Citation verification for scientific manuscripts.

Queries the local Paperpile mirror (DOI-direct) first, then falls back to
Semantic Scholar, CrossRef, and OpenAlex to verify that references in a
markdown manuscript are real and correctly attributed.

Usage:
    python3 verify_citations.py manuscript.md [-o report.md]
    python3 verify_citations.py --refs-only references.txt [-o report.md]
    python3 verify_citations.py manuscript.md --no-paperpile  # external only

Requirements:
    - Python 3.9+ (uses Optional[] from typing; NOT the 3.10+ dict|None syntax)
    - Run with /opt/homebrew/bin/python3.13 or any Python 3.9+ interpreter
    - Requires a populated ## References section in the manuscript.
      If the manuscript uses only inline citations with no bibliography,
      the script reports "No references found." In that case, extract
      inline citations manually and use --refs-only with a plain-text list.
"""

import json
import os
import re
import sys
import time
import urllib.request
import urllib.parse
from pathlib import Path
from typing import Optional

# API endpoints
S2_SEARCH = "https://api.semanticscholar.org/graph/v1/paper/search"
CROSSREF_WORKS = "https://api.crossref.org/works"
OPENALEX_WORKS = "https://api.openalex.org/works"

MAILTO = "simon@marinemegafauna.org"  # CrossRef polite pool

# Paperpile mirror — local DOI-direct lookup
VAULT_ROOT = Path(
    "/Users/simonjpierce/Library/Mobile Documents/iCloud~md~obsidian/Documents/Simon's Vault"
)
PAPERPILE_DIR = VAULT_ROOT / "02_MARINE MEGAFAUNA" / "REFERENCE LIBRARY" / "Paperpile Library"
PAPERPILE_BUILD_STATUS = PAPERPILE_DIR / "_meta" / "build-status"
PAPERPILE_STATE_JSON = PAPERPILE_DIR / "_meta" / "state.json"
PAPERPILE_PAPERS_REL = "02_MARINE MEGAFAUNA/REFERENCE LIBRARY/Paperpile Library/papers"

# Lazy/cached module-level state for the mirror.
_MIRROR_DISABLED = False  # toggled by --no-paperpile / env var
_MIRROR_AVAILABILITY: Optional[bool] = None  # None until first probe
_MIRROR_STATE: Optional[dict] = None  # full state.json dict
_MIRROR_DOI_INDEX: Optional[dict[str, str]] = None  # normalised_doi -> pub_id


def set_paperpile_disabled(disabled: bool) -> None:
    """Disable in-library lookup for the rest of the process."""
    global _MIRROR_DISABLED, _MIRROR_AVAILABILITY
    _MIRROR_DISABLED = disabled
    if disabled:
        _MIRROR_AVAILABILITY = False


def _mirror_available() -> bool:
    """Probe the build-status gate and load state.json lazily.

    Returns True only when status == 'ready' AND state.json loaded
    AND the DOI alias index is reachable. Any failure latches False
    for the remainder of the run.
    """
    global _MIRROR_AVAILABILITY, _MIRROR_STATE, _MIRROR_DOI_INDEX
    if _MIRROR_DISABLED:
        return False
    if _MIRROR_AVAILABILITY is not None:
        return _MIRROR_AVAILABILITY
    try:
        status_text = PAPERPILE_BUILD_STATUS.read_text(encoding="utf-8")
        status = json.loads(status_text)
        if status.get("status") != "ready":
            print(
                f"  [paperpile] build-status not ready ({status.get('status')!r}); "
                f"skipping in-library lookup.",
                file=sys.stderr,
            )
            _MIRROR_AVAILABILITY = False
            return False
    except FileNotFoundError:
        _MIRROR_AVAILABILITY = False
        return False
    except Exception as e:
        print(f"  [paperpile] build-status unreadable ({e}); skipping in-library lookup.",
              file=sys.stderr)
        _MIRROR_AVAILABILITY = False
        return False

    try:
        with PAPERPILE_STATE_JSON.open("r", encoding="utf-8") as fh:
            _MIRROR_STATE = json.load(fh)
    except Exception as e:
        print(f"  [paperpile] state.json unreadable ({e}); skipping in-library lookup.",
              file=sys.stderr)
        _MIRROR_AVAILABILITY = False
        return False

    raw_aliases = (_MIRROR_STATE.get("aliases") or {}).get("doi") or {}
    # Build normalised-DOI index. Skip keys that aren't DOI-shaped (the live
    # alias table contains a few stragglers like a URL pointing at an IUCN PDF).
    index: dict[str, str] = {}
    for raw_doi, pub_id in raw_aliases.items():
        if not isinstance(raw_doi, str) or not raw_doi.startswith("10."):
            continue
        nd = _normalise_doi(raw_doi)
        if nd:
            index[nd] = pub_id
    _MIRROR_DOI_INDEX = index
    _MIRROR_AVAILABILITY = True
    return True


def _normalise_doi(doi: str) -> str:
    """Lowercase, strip URL/handle prefixes and Markdown/punctuation wrappers."""
    if not doi:
        return ""
    s = doi.strip()
    # Strip Markdown link wrappers like `[Guerra 2017](https://doi.org/10.x)` —
    # we already extracted the URL, but if a raw `[doi]` form sneaks through,
    # nibble leading `[` and trailing `]` plus parenthesised tails.
    s = s.strip("[]")
    # Iteratively strip recognised prefixes (case-insensitive).
    lowered_prefixes = [
        "https://dx.doi.org/",
        "http://dx.doi.org/",
        "https://doi.org/",
        "http://doi.org/",
        "dx.doi.org/",
        "doi.org/",
        "doi:",
        "doi ",
    ]
    sl = s.lower()
    changed = True
    while changed:
        changed = False
        for p in lowered_prefixes:
            if sl.startswith(p):
                s = s[len(p):].lstrip()
                sl = s.lower()
                changed = True
                break
    # Trim trailing wrapper punctuation: `.`, `,`, `;`, `)`, `]`, `>`, `}`,
    # whitespace, `/`.
    s = s.rstrip(".,;)>]}/ \t\r\n")
    # Final lowercase for case-insensitive matching.
    return s.lower()


_DOI_REGEX = re.compile(r"(?i)\b10\.\d{4,9}/\S+")


def _extract_doi(text: str) -> Optional[str]:
    """Extract a DOI from a reference string, normalised. None if no DOI present."""
    if not text:
        return None
    m = _DOI_REGEX.search(text)
    if not m:
        return None
    candidate = m.group(0)
    return _normalise_doi(candidate) or None


def lookup_in_paperpile(doi: str) -> tuple[Optional[dict], Optional[str]]:
    """Look up a normalised DOI in the local Paperpile mirror.

    Returns (paper_record, vault_relative_note_path) on hit, (None, None) on miss
    or any drift case (stale alias, missing record, DOI inequality, missing slug,
    missing note file).
    """
    if not _mirror_available():
        return (None, None)
    if not doi:
        return (None, None)
    assert _MIRROR_STATE is not None and _MIRROR_DOI_INDEX is not None
    normalised = _normalise_doi(doi)
    pub_id = _MIRROR_DOI_INDEX.get(normalised)
    if not pub_id:
        return (None, None)
    record = (_MIRROR_STATE.get("paper_records") or {}).get(pub_id)
    if not record:
        # Stale alias after merge — fall through.
        return (None, None)
    if _normalise_doi(record.get("doi") or "") != normalised:
        # Alias drift (DOI corrected in Paperpile but alias not pruned).
        return (None, None)
    slug = record.get("slug")
    if not slug:
        return (None, None)
    note_rel = f"{PAPERPILE_PAPERS_REL}/{slug}.md"
    note_abs = VAULT_ROOT / note_rel
    if not note_abs.exists():
        # Writer/state drift — fall through to external waterfall.
        return (None, None)
    return (record, note_rel)


def _check_inlibrary_consistency(parsed: dict, record: dict) -> list[str]:
    """Compare manuscript-cited author/year against the curated paper_record.

    Returns a list of issues. Empty list means clean — status VERIFIED.
    Non-empty means status CONFLICT.
    """
    issues: list[str] = []
    # Author check: paper_record stores authors_resolved[0]['display'] (full name);
    # the manuscript reference's first_author is usually a surname only.
    resolved = record.get("authors_resolved") or []
    if resolved:
        found_display = (resolved[0] or {}).get("display") or ""
        ref_author = parsed.get("first_author", "")
        if found_display and ref_author:
            issue = _check_author(ref_author, found_display)
            if issue:
                issues.append(issue)
    # Year check: ±1 year tolerance for preprint→published transitions.
    rec_year = record.get("year")
    ref_year = parsed.get("year")
    if rec_year and ref_year and abs(int(rec_year) - int(ref_year)) > 1:
        issues.append(f"Year mismatch: ref={ref_year}, found={rec_year}")
    # No title check — DOI is the identity; styles vary.
    return issues


_REFERENCES_HEADING_PATTERN = re.compile(
    r"^##\s*\**\s*(?:"
    r"[\w\s]*References?(?:\s+Cited)?|"
    r"Reference\s+List|"
    r"Bibliography|"
    r"Literature\s+Cited|"
    r"Works\s+Cited|"
    r"Cited\s+Works|"
    r"Citations|"
    r"Sources|"
    r"REFERENCES[\w\s]*"
    r")\s*\**",
    re.IGNORECASE | re.MULTILINE,
)


def extract_references(text: str) -> list[str]:
    """Extract individual references from all References sections of a manuscript."""
    ref_pattern = _REFERENCES_HEADING_PATTERN

    # Find ALL reference sections (some manuscripts split into multiple)
    ref_text_parts: list[str] = []
    for match in ref_pattern.finditer(text):
        section = text[match.end() :]
        # Stop at next non-reference H2 heading or end of file
        next_heading = re.search(r"^##\s", section, re.MULTILINE)
        if next_heading:
            section = section[: next_heading.start()]
        ref_text_parts.append(section)

    if not ref_text_parts:
        return []

    ref_text = "\n\n".join(ref_text_parts)

    # Split into individual references.
    # Each reference starts after a blank line with an author name (uppercase letter).
    refs: list[str] = []
    current: list[str] = []
    for line in ref_text.strip().split("\n"):
        line = line.strip()
        # Strip bullet prefix and markdown italic markers
        line = re.sub(r"^[-*]\s+", "", line)
        line = line.replace("_", "")
        if not line:
            if current:
                refs.append(" ".join(current))
                current = []
            continue
        # New reference starts with an author surname and current ref already has a year
        if (
            current
            and re.match(r"^[A-Z][a-zéèêëü]", line)
            and re.search(r"\(\d{4}\)", " ".join(current))
        ):
            refs.append(" ".join(current))
            current = [line]
        else:
            current.append(line)
    if current:
        refs.append(" ".join(current))

    # Deduplicate by first author + year
    seen: set[str] = set()
    unique: list[str] = []
    for r in refs:
        if not re.search(r"\(\d{4}\)", r):
            continue
        # Key on normalized first ~40 chars (author + year)
        key = re.sub(r"[^a-z0-9]", "", r[:40].lower())
        if key not in seen:
            seen.add(key)
            unique.append(r)
    return unique


def parse_reference(ref: str) -> dict:
    """Parse a reference string into components."""
    result: dict = {"full": ref}

    # Extract year
    year_match = re.search(r"\((\d{4})\)", ref)
    if year_match:
        result["year"] = int(year_match.group(1))

    # Extract first author surname (before first comma or initials)
    author_match = re.match(r"^([A-Z][a-zéèêëü'\-]+(?:\s[A-Z][a-zéèêëü'\-]+)*)", ref)
    if author_match:
        result["first_author"] = author_match.group(1)

    # Extract title: text between closing year paren and the journal name.
    # Titles end with . or ? or ! followed by a space. Use the LAST sentence
    # terminator before what looks like a journal name (capitalised words or italics).
    if year_match:
        after_year = ref[year_match.end() :].strip()
        # Try to find title ending with sentence punctuation followed by journal
        title_match = re.match(r"(.+?[.?!])\s+(?:[A-Z])", after_year)
        if title_match:
            result["title"] = title_match.group(1).strip().rstrip(".")
        else:
            # Fallback: take first 100 chars as search query
            result["title"] = after_year[:100].strip()

    # Extract DOI (normalised) — used both for in-library lookup and as a hint
    # downstream. Done here so verify_one can consult it before the title guard.
    doi = _extract_doi(ref)
    if doi:
        result["doi"] = doi

    return result


def _api_get(url: str, timeout: int = 15) -> Optional[dict]:
    """GET request returning parsed JSON, or None on any failure."""
    try:
        req = urllib.request.Request(url)
        req.add_header("User-Agent", f"citation-verify/1.0 (mailto:{MAILTO})")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read())
    except Exception:
        return None


def search_semantic_scholar(title: str, year: Optional[int] = None) -> Optional[dict]:
    """Search Semantic Scholar for a paper by title."""
    query = urllib.parse.quote(title[:200])
    url = f"{S2_SEARCH}?query={query}&limit=5&fields=title,authors,year,venue,externalIds"
    data = _api_get(url)
    if not data:
        return None
    for paper in data.get("data", []):
        if year and paper.get("year") and abs(paper["year"] - year) > 1:
            continue
        return paper
    return None


def search_crossref(title: str, author: Optional[str] = None) -> Optional[dict]:
    """Search CrossRef for a paper by title."""
    params: dict[str, str] = {
        "query.bibliographic": title[:200],
        "rows": "3",
        "mailto": MAILTO,
    }
    if author:
        params["query.author"] = author
    url = f"{CROSSREF_WORKS}?{urllib.parse.urlencode(params)}"
    data = _api_get(url)
    if not data:
        return None
    items = data.get("message", {}).get("items", [])
    return items[0] if items else None


def search_openalex(title: str) -> Optional[dict]:
    """Search OpenAlex for a paper by title."""
    query = urllib.parse.quote(title[:200])
    url = f"{OPENALEX_WORKS}?search={query}&per_page=3&mailto={MAILTO}"
    data = _api_get(url)
    if not data:
        return None
    results = data.get("results", [])
    return results[0] if results else None


def normalize(s: str) -> str:
    """Lowercase, strip punctuation for fuzzy comparison."""
    return re.sub(r"[^a-z0-9 ]", "", s.lower()).strip()


def title_similarity(a: str, b: str) -> float:
    """Word-overlap similarity between two titles."""
    words_a = set(normalize(a).split())
    words_b = set(normalize(b).split())
    if not words_a or not words_b:
        return 0.0
    return len(words_a & words_b) / max(len(words_a), len(words_b))


def _check_author(ref_author: str, found_name: str) -> Optional[str]:
    """Return an issue string if the first author doesn't match, else None."""
    if not ref_author or not found_name:
        return None
    ra = normalize(ref_author)
    fn = normalize(found_name)
    if ra in fn or fn in ra:
        return None
    # Check just the surname portion
    ra_parts = ra.split()
    fn_parts = fn.split()
    if ra_parts and fn_parts and (ra_parts[-1] in fn_parts or fn_parts[-1] in ra_parts):
        return None
    return f"First author mismatch: ref='{ref_author}', found='{found_name}'"


def verify_one(parsed: dict) -> dict:
    """Verify a single parsed reference against the local mirror, then APIs."""
    result = {
        "reference": parsed.get("full", ""),
        "first_author": parsed.get("first_author", ""),
        "year": parsed.get("year"),
        "title_query": parsed.get("title", ""),
        "status": "NOT_FOUND",
        "issues": [],
        "doi": None,
        "matched_title": None,
        "source_api": None,
        "paperpile_note": None,
        "paperpile_pub_id": None,
    }

    # --- Paperpile in-library lookup (DOI-direct) ---
    # Done BEFORE the title parse-error guard so DOI-bearing references with
    # weak title extraction still resolve locally.
    cited_doi = parsed.get("doi")
    if cited_doi and _mirror_available():
        record, note_rel = lookup_in_paperpile(cited_doi)
        if record:
            issues = _check_inlibrary_consistency(parsed, record)
            result["source_api"] = "Paperpile (in-library)"
            result["doi"] = record.get("doi")  # canonical, raw-case from record
            result["matched_title"] = record.get("title")
            result["paperpile_note"] = note_rel
            result["paperpile_pub_id"] = record.get("pub_id")
            result["issues"] = issues
            result["status"] = "CONFLICT" if issues else "VERIFIED"
            return result

    title = parsed.get("title", "")
    if not title or len(title) < 10:
        result["status"] = "PARSE_ERROR"
        result["issues"].append("Could not extract title from reference")
        return result

    year = parsed.get("year")
    first_author = parsed.get("first_author", "")
    sim_threshold = 0.45

    # --- Semantic Scholar ---
    s2 = search_semantic_scholar(title, year)
    if s2 and title_similarity(title, s2.get("title", "")) > sim_threshold:
        result["source_api"] = "Semantic Scholar"
        result["matched_title"] = s2.get("title")
        result["doi"] = (s2.get("externalIds") or {}).get("DOI")
        issues = []
        if year and s2.get("year") and abs(s2["year"] - year) > 1:
            issues.append(f"Year mismatch: ref={year}, found={s2['year']}")
        s2_authors = s2.get("authors", [])
        if first_author and s2_authors:
            author_issue = _check_author(first_author, s2_authors[0].get("name", ""))
            if author_issue:
                issues.append(author_issue)
        result["issues"] = issues
        result["status"] = "VERIFIED" if not issues else "PARTIAL_MATCH"
        return result

    time.sleep(0.3)

    # --- CrossRef ---
    cr = search_crossref(title, first_author)
    if cr:
        cr_title = (cr.get("title") or [""])[0]
        if title_similarity(title, cr_title) > sim_threshold:
            result["source_api"] = "CrossRef"
            result["matched_title"] = cr_title
            result["doi"] = cr.get("DOI")
            issues = []
            cr_year = None
            for df in ("published-print", "published-online", "published"):
                dp = cr.get(df, {}).get("date-parts", [[]])
                if dp and dp[0]:
                    cr_year = dp[0][0]
                    break
            if year and cr_year and abs(cr_year - year) > 1:
                issues.append(f"Year mismatch: ref={year}, found={cr_year}")
            cr_authors = cr.get("author", [])
            if first_author and cr_authors:
                author_issue = _check_author(
                    first_author, cr_authors[0].get("family", "")
                )
                if author_issue:
                    issues.append(author_issue)
            result["issues"] = issues
            result["status"] = "VERIFIED" if not issues else "PARTIAL_MATCH"
            return result

    time.sleep(0.3)

    # --- OpenAlex ---
    oa = search_openalex(title)
    if oa:
        oa_title = oa.get("display_name", "")
        if title_similarity(title, oa_title) > sim_threshold:
            result["source_api"] = "OpenAlex"
            result["matched_title"] = oa_title
            doi = oa.get("doi", "")
            result["doi"] = doi.replace("https://doi.org/", "") if doi else None
            issues = []
            oa_year = oa.get("publication_year")
            if year and oa_year and abs(oa_year - year) > 1:
                issues.append(f"Year mismatch: ref={year}, found={oa_year}")
            oa_authors = oa.get("authorships", [])
            if first_author and oa_authors:
                author_issue = _check_author(
                    first_author,
                    oa_authors[0].get("author", {}).get("display_name", ""),
                )
                if author_issue:
                    issues.append(author_issue)
            result["issues"] = issues
            result["status"] = "VERIFIED" if not issues else "PARTIAL_MATCH"
            return result

    return result


def verify_references(refs: list[str]) -> list[dict]:
    """Verify a list of reference strings."""
    print(f"Verifying {len(refs)} references...", file=sys.stderr)
    results = []
    status_icon = {
        "VERIFIED": "✓",
        "PARTIAL_MATCH": "~",
        "NOT_FOUND": "✗",
        "PARSE_ERROR": "?",
        "CONFLICT": "!",
    }
    for i, ref in enumerate(refs):
        parsed = parse_reference(ref)
        print(
            f"  [{i + 1}/{len(refs)}] {parsed.get('first_author', '?')} "
            f"({parsed.get('year', '?')})...",
            file=sys.stderr,
        )
        result = verify_one(parsed)
        # Use ✓P prefix for Paperpile in-library hits (verified or conflict)
        is_pp = result.get("source_api") == "Paperpile (in-library)"
        base = status_icon.get(result["status"], "?")
        icon = f"{base}P" if is_pp and result["status"] in ("VERIFIED", "CONFLICT") else base
        suffix = ""
        if is_pp:
            if result["status"] == "VERIFIED":
                suffix = " (Paperpile in-library)"
            elif result["status"] == "CONFLICT":
                detail = "; ".join(result.get("issues") or []) or "in-library record disagrees"
                suffix = f" (Paperpile in-library: {detail})"
        elif result.get("source_api"):
            suffix = f" ({result['source_api']})"
        print(f"    {icon} {result['status']}{suffix}", file=sys.stderr)
        results.append(result)
        # Skip the politeness sleep when the result came from local mirror —
        # no external API was hit, so no rate limit to honour.
        if not is_pp:
            time.sleep(0.5)
    return results


def _has_references_heading(text: str) -> bool:
    """Check if the text contains a References-style H2 heading."""
    return bool(_REFERENCES_HEADING_PATTERN.search(text))


def extract_cited_dois_from_document(text: str) -> tuple[list[str], str]:
    """Extract every unique normalised DOI cited in a document.

    Tries a headed References/Bibliography/Sources section first via
    `extract_references` + `parse_reference`. If no such section exists,
    falls back to `_DOI_REGEX.finditer` over the full document body.

    Returns `(dois, extraction_path)` where `extraction_path` is either
    `"headed"` (DOIs came from a recognised references section) or
    `"full_document_fallback"` (no headed section; pulled DOIs from prose).

    Order of first appearance is preserved. The hard no-external-API
    invariant lives in the caller; this helper is local-only.
    """
    refs = extract_references(text)
    extraction_path = "headed" if refs else "full_document_fallback"

    seen: set[str] = set()
    dois: list[str] = []

    if refs:
        for ref in refs:
            parsed = parse_reference(ref)
            doi = parsed.get("doi")
            if doi and doi not in seen:
                seen.add(doi)
                dois.append(doi)
    else:
        # Full-document fallback — use finditer (match-all), not _extract_doi
        # (which is single-reference / single-DOI). Per Codex H1.
        for m in _DOI_REGEX.finditer(text):
            doi = _normalise_doi(m.group(0))
            if doi and doi not in seen:
                seen.add(doi)
                dois.append(doi)

    return dois, extraction_path


def _mirror_metadata() -> tuple[str, Optional[str], Optional[str]]:
    """Return (status, build_id, unavailable_reason) for the Paperpile mirror.

    `status` is one of:
      - "ready"        — build-status reports ready, state.json loaded OK
      - "building"     — build-status status field reports a non-ready state
      - "unavailable"  — build-status missing, unreadable, or state.json broken

    `build_id` is the build-status `build_id` when known, else None.
    `unavailable_reason` is a short human-readable string when status != "ready",
    else None.
    """
    if _MIRROR_DISABLED:
        return ("unavailable", None, "mirror disabled (--no-paperpile)")
    try:
        status_text = PAPERPILE_BUILD_STATUS.read_text(encoding="utf-8")
        status = json.loads(status_text)
    except FileNotFoundError:
        return ("unavailable", None, "build-status file missing")
    except Exception as e:
        return ("unavailable", None, f"build-status unreadable: {e}")

    build_id = status.get("build_id")
    raw_status = status.get("status")
    if raw_status != "ready":
        return (str(raw_status or "unavailable"), build_id, f"build-status: {raw_status!r}")

    # Status is ready; force state.json load so callers see the same gate
    # `_mirror_available` enforces.
    if not _mirror_available():
        return ("unavailable", build_id, "state.json unreadable")
    return ("ready", build_id, None)


def verify_manuscript(path: Path) -> list[dict]:
    """Verify all citations in a manuscript file."""
    text = path.read_text()
    refs = extract_references(text)
    if not refs:
        if _has_references_heading(text):
            print(
                f"References section found in {path.name} but no parseable references "
                f"(short-form or non-standard format). Manual verification required.",
                file=sys.stderr,
            )
        else:
            print(f"No references section found in {path.name}", file=sys.stderr)
        return []
    return verify_references(refs)


def format_report(results: list[dict], source: str) -> str:
    """Format verification results as a markdown report.

    Section order: Not Found → Conflicts → Partial Matches → Verified → Parse Errors.
    The Verified section emits a wikilink to the Paperpile note when available.
    Each section line includes the literal status token so downstream callers
    that substring-count (e.g. nightly_workhorse) can detect entries.
    """
    verified = [r for r in results if r["status"] == "VERIFIED"]
    partial = [r for r in results if r["status"] == "PARTIAL_MATCH"]
    not_found = [r for r in results if r["status"] == "NOT_FOUND"]
    parse_errors = [r for r in results if r["status"] == "PARSE_ERROR"]
    conflicts = [r for r in results if r["status"] == "CONFLICT"]
    in_library = [r for r in results if r.get("source_api") == "Paperpile (in-library)"]

    lines = [
        "# Citation Verification Report",
        "",
        f"**Source:** `{source}`",
        f"**Date:** {time.strftime('%Y-%m-%d %H:%M')}",
        f"**Total references:** {len(results)}",
        f"**Paperpile in-library hits:** {len(in_library)}",
        "",
        "| Status | Count |",
        "|--------|-------|",
        f"| Verified | {len(verified)} |",
        f"| Conflict (in-library) | {len(conflicts)} |",
        f"| Partial match | {len(partial)} |",
        f"| Not found | {len(not_found)} |",
        f"| Parse error | {len(parse_errors)} |",
        "",
    ]

    if not_found:
        lines.append("## Not Found — Verify Manually")
        lines.append("")
        lines.append("These references could not be matched in any database. They may be")
        lines.append("fabricated, have incorrect details, or be too obscure for the APIs.")
        lines.append("")
        for r in not_found:
            lines.append(
                f"- **NOT_FOUND** — {r['first_author']} ({r['year']}): "
                f"{r['reference'][:200]}"
            )
        lines.append("")

    if conflicts:
        lines.append("## Conflicts — In-library record disagrees with cited reference")
        lines.append("")
        lines.append(
            "The DOI matches a paper in your curated Paperpile library, but the "
            "manuscript's author/year identity disagrees with the curated record. "
            "The library is the source of truth — likely a citation identity error "
            "in the manuscript (wrong author, wrong year, or wrong DOI). "
            "Representation accuracy (whether the manuscript faithfully reports "
            "what the paper actually said) is a separate check — see /red-team "
            "Step 1b's curated literature pack."
        )
        lines.append("")
        for r in conflicts:
            lines.append(f"**CONFLICT** — {r['first_author']} ({r['year']})")
            lines.append(f"- Ref: {r['reference'][:200]}")
            if r.get("doi"):
                lines.append(f"- DOI: {r['doi']}")
            if r.get("matched_title"):
                lines.append(f"- In-library title: {r['matched_title']}")
            if r.get("paperpile_note"):
                lines.append(f"- Paperpile note: [[{r['paperpile_note']}]]")
            for issue in r["issues"]:
                lines.append(f"- **Issue:** {issue}")
            lines.append("")

    if partial:
        lines.append("## Partial Matches — Issues Found")
        lines.append("")
        for r in partial:
            lines.append(f"**PARTIAL_MATCH** — {r['first_author']} ({r['year']})")
            lines.append(f"- Ref: {r['reference'][:150]}...")
            lines.append(f"- Matched: {r['matched_title']}")
            if r["doi"]:
                lines.append(f"- DOI: {r['doi']}")
            for issue in r["issues"]:
                lines.append(f"- **Issue:** {issue}")
            lines.append(f"- Source: {r['source_api']}")
            lines.append("")

    if verified:
        lines.append("## Verified")
        lines.append("")
        for r in verified:
            doi_str = f" — DOI: {r['doi']}" if r["doi"] else ""
            lines.append(
                f"- **VERIFIED** — {r['first_author']} ({r['year']}){doi_str} "
                f"[{r['source_api']}]"
            )
            if r.get("paperpile_note"):
                lines.append(f"  → [[{r['paperpile_note']}]]")
        lines.append("")

    if parse_errors:
        lines.append("## Parse Errors")
        lines.append("")
        for r in parse_errors:
            lines.append(f"- **PARSE_ERROR** — {r['reference'][:200]}")
        lines.append("")

    return "\n".join(lines)


def patch_dois(manuscript_path: Path, results: list[dict]) -> int:
    """Insert missing DOIs into manuscript references. Returns count of DOIs added."""
    text = manuscript_path.read_text()
    patched = 0

    for r in results:
        if r["status"] not in ("VERIFIED", "PARTIAL_MATCH"):
            continue
        doi = r.get("doi")
        if not doi:
            continue

        ref_text = r["reference"]
        # Skip if the reference already has a DOI
        if "doi.org" in ref_text.lower() or re.search(r"\bDOI\b", ref_text):
            continue

        # Find this reference in the manuscript text.
        # Use first author + year as anchor (ref_text may have been cleaned).
        author = r.get("first_author", "")
        year = r.get("year")
        if not author or not year:
            continue

        # Build a pattern to find this specific reference line
        # Match: author name ... (year) ... end-of-reference (newline or end)
        escaped_author = re.escape(author)
        pattern = re.compile(
            rf"({escaped_author}.*?\({year}\).*?)(\n\n|\n(?=[A-Z])|$)",
            re.DOTALL,
        )
        match = pattern.search(text)
        if not match:
            continue

        ref_in_text = match.group(1).rstrip()
        doi_url = f" https://doi.org/{doi}"

        # Only insert if the DOI isn't already there
        if doi_url not in text:
            text = text.replace(ref_in_text, ref_in_text + doi_url, 1)
            patched += 1

    if patched > 0:
        manuscript_path.write_text(text)
    return patched


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Verify citations in a scientific manuscript"
    )
    parser.add_argument("manuscript", help="Path to markdown manuscript")
    parser.add_argument("-o", "--output", help="Output report path (default: stdout)")
    parser.add_argument(
        "--refs-only",
        action="store_true",
        help="Treat input as a plain references list (no manuscript parsing)",
    )
    parser.add_argument(
        "--patch-dois",
        action="store_true",
        help="Insert missing DOIs into manuscript references (modifies the file)",
    )
    parser.add_argument(
        "--no-paperpile",
        action="store_true",
        help="Skip the local Paperpile in-library DOI lookup (external APIs only)",
    )
    parser.add_argument(
        "--extract-and-lookup-only",
        action="store_true",
        help=(
            "Extract all cited DOIs from the document, look each up in the local "
            "Paperpile mirror, and emit JSON describing in-library hits and misses. "
            "NEVER calls Semantic Scholar / CrossRef / OpenAlex. Requires -o "
            "<output.json>. Used by /red-team's curated-literature pack builder."
        ),
    )
    args = parser.parse_args()

    # Env-var emergency override (parity with --no-paperpile).
    if args.no_paperpile or os.environ.get("VERIFY_CITATIONS_NO_PAPERPILE") == "1":
        set_paperpile_disabled(True)

    path = Path(args.manuscript)
    if not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
        sys.exit(1)

    if args.extract_and_lookup_only:
        if not args.output:
            print(
                "--extract-and-lookup-only requires -o <output.json>",
                file=sys.stderr,
            )
            sys.exit(2)
        text = path.read_text()
        dois, extraction = extract_cited_dois_from_document(text)
        mirror_status, build_id, unavailable_reason = _mirror_metadata()
        hits: list[dict] = []
        misses: list[dict] = []
        for doi in dois:
            if mirror_status != "ready":
                misses.append(
                    {"cited_doi": doi, "reason": unavailable_reason or mirror_status}
                )
                continue
            record, note_rel = lookup_in_paperpile(doi)
            if record:
                hits.append(
                    {
                        "cited_doi": doi,
                        "pub_id": record.get("pub_id"),
                        "note_rel": note_rel,
                        "year": record.get("year"),
                        "title": record.get("title"),
                        "journal": record.get("journal")
                        or record.get("journal_full"),
                        "slug": record.get("slug"),
                        "paperpile_labels": record.get("paperpile_labels") or [],
                        "has_abstract": bool(record.get("abstract")),
                        "has_highlights": bool(record.get("highlights")),
                    }
                )
            else:
                misses.append({"cited_doi": doi, "reason": "not_in_library"})
        output = {
            "document": str(path),
            "extraction": extraction,
            "mirror_status": mirror_status,
            "build_id": build_id,
            "unavailable_reason": unavailable_reason,
            "total_cited_dois": len(dois),
            "hits": hits,
            "misses": misses,
        }
        Path(args.output).write_text(json.dumps(output, indent=2, ensure_ascii=False))
        print(
            f"[extract-and-lookup] {len(hits)}/{len(dois)} cited DOIs in-library "
            f"(extraction: {extraction}, mirror_status: {mirror_status})",
            file=sys.stderr,
        )
        # NO external API calls. NO verify_one. NO Semantic Scholar / CrossRef / OpenAlex.
        return

    if args.refs_only:
        text = path.read_text()
        refs = [
            line.strip()
            for line in text.split("\n\n")
            if line.strip() and re.search(r"\(\d{4}\)", line)
        ]
        if not refs:
            print("No references found in input.", file=sys.stderr)
            sys.exit(1)
        results = verify_references(refs)
    else:
        results = verify_manuscript(path)
        if not results:
            # Clean exit — missing/unparseable references is a known limitation, not an error.
            # Callers (e.g. nightly workhorse) treat exit 1 as a task failure.
            sys.exit(0)

    report = format_report(results, str(path))

    if args.output:
        Path(args.output).write_text(report)
        print(f"\nReport written to {args.output}", file=sys.stderr)
    else:
        print(report)

    if args.patch_dois and not args.refs_only:
        count = patch_dois(path, results)
        if count:
            print(f"\nPatched {count} DOI(s) into {path.name}", file=sys.stderr)
        else:
            print("\nNo DOIs to patch (all present or none found).", file=sys.stderr)


if __name__ == "__main__":
    main()
