#!/usr/bin/env python3
"""Citation verification for scientific manuscripts.

Queries Semantic Scholar, CrossRef, and OpenAlex to verify that
references in a markdown manuscript are real and correctly attributed.

Usage:
    python3 verify_citations.py manuscript.md [-o report.md]
    python3 verify_citations.py --refs-only references.txt [-o report.md]

Requirements:
    - Python 3.9+ (uses Optional[] from typing; NOT the 3.10+ dict|None syntax)
    - Run with /opt/homebrew/bin/python3.13 or any Python 3.9+ interpreter
    - Requires a populated ## References section in the manuscript.
      If the manuscript uses only inline citations with no bibliography,
      the script reports "No references found." In that case, extract
      inline citations manually and use --refs-only with a plain-text list.
"""

import json
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


def extract_references(text: str) -> list[str]:
    """Extract individual references from all References sections of a manuscript."""
    ref_pattern = re.compile(
        r"^##\s*\**\s*(?:[\w\s]*References?|Bibliography|Literature Cited|REFERENCES[\w\s]*)\s*\**",
        re.IGNORECASE | re.MULTILINE,
    )

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
    """Verify a single parsed reference against APIs."""
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
    }

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
    for i, ref in enumerate(refs):
        parsed = parse_reference(ref)
        print(
            f"  [{i + 1}/{len(refs)}] {parsed.get('first_author', '?')} "
            f"({parsed.get('year', '?')})...",
            file=sys.stderr,
        )
        result = verify_one(parsed)
        status_icon = {"VERIFIED": "✓", "PARTIAL_MATCH": "~", "NOT_FOUND": "✗", "PARSE_ERROR": "?"}
        print(f"    {status_icon.get(result['status'], '?')} {result['status']}", file=sys.stderr)
        results.append(result)
        time.sleep(0.5)  # Be polite to APIs
    return results


def _has_references_heading(text: str) -> bool:
    """Check if the text contains a References-style H2 heading."""
    ref_pattern = re.compile(
        r"^##\s*\**\s*(?:[\w\s]*References?|Bibliography|Literature Cited|REFERENCES[\w\s]*)\s*\**",
        re.IGNORECASE | re.MULTILINE,
    )
    return bool(ref_pattern.search(text))


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
    """Format verification results as a markdown report."""
    verified = [r for r in results if r["status"] == "VERIFIED"]
    partial = [r for r in results if r["status"] == "PARTIAL_MATCH"]
    not_found = [r for r in results if r["status"] == "NOT_FOUND"]
    parse_errors = [r for r in results if r["status"] == "PARSE_ERROR"]

    lines = [
        "# Citation Verification Report",
        "",
        f"**Source:** `{source}`",
        f"**Date:** {time.strftime('%Y-%m-%d %H:%M')}",
        f"**Total references:** {len(results)}",
        "",
        "| Status | Count |",
        "|--------|-------|",
        f"| Verified | {len(verified)} |",
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
                f"- **{r['first_author']} ({r['year']})**: "
                f"{r['reference'][:200]}"
            )
        lines.append("")

    if partial:
        lines.append("## Partial Matches — Issues Found")
        lines.append("")
        for r in partial:
            lines.append(f"**{r['first_author']} ({r['year']})**")
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
                f"- {r['first_author']} ({r['year']}){doi_str} "
                f"[{r['source_api']}]"
            )
        lines.append("")

    if parse_errors:
        lines.append("## Parse Errors")
        lines.append("")
        for r in parse_errors:
            lines.append(f"- {r['reference'][:200]}")
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
    args = parser.parse_args()

    path = Path(args.manuscript)
    if not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
        sys.exit(1)

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
