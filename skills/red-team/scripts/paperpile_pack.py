#!/usr/bin/env python3
"""Curated literature pack builder for /red-team Step 1b.

Reads the document under review, invokes verify_citations.py with the
--extract-and-lookup-only flag to discover which cited DOIs exist in
Simon's Paperpile mirror, reads the in-library paper notes, and writes
a curated literature pack at /tmp/red-team-paperpile-pack.md.

The pack is included as a context document in:
  - the Step 2 subagent prompt
  - the Step 6a Gemini prompt
  - the Step 6d Codex prompt
  - the Step 6g --parallel-mode prompts

Skip rules (per spec §1b.0):
  - document type is process doc / spec / internal note → caller skips
  - no References heading AND no DOI-shaped strings in the body
  - Paperpile mirror build-status != "ready"
  - --no-paperpile-pack flag passed to /red-team

Stdlib only. Safe to call from any subprocess context.

Usage:
    python3 paperpile_pack.py <document.md> [-o /tmp/red-team-paperpile-pack.md]

JSON contract validated before pack assembly (per spec Touch points,
prevents mirror-unavailable being silently misreported as zero coverage).
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Optional

VAULT_ROOT = Path(
    "/Users/simonjpierce/Library/Mobile Documents/iCloud~md~obsidian/Documents/Simon's Vault"
)
PAPERPILE_REL = "02_MARINE MEGAFAUNA/REFERENCE LIBRARY/Paperpile Library"
VERIFY_CITATIONS = Path(
    os.path.expanduser("~/.claude/skills/verify-citations/verify_citations.py")
)
DEFAULT_OUTPUT = Path("/tmp/red-team-paperpile-pack.md")

# Pack policy defaults (per spec §1b.3, §1b.4)
ABSTRACT_WORD_CAP = 250
HIGHLIGHTS_PER_PAPER_CAP = 3
DEFAULT_TOP_N = 20
LONG_DOC_WORD_THRESHOLD = 8000  # matches red-team SKILL.md:47 long-doc flag
LONG_DOC_TOP_N = 10


REQUIRED_JSON_FIELDS = {
    "document",
    "extraction",
    "mirror_status",
    "build_id",
    "unavailable_reason",
    "total_cited_dois",
    "hits",
    "misses",
}


class PackError(RuntimeError):
    """Raised on any failure that should cause /red-team to skip the pack."""


def _run_verify_citations(document: Path, output: Path) -> dict:
    """Invoke verify_citations.py --extract-and-lookup-only; return parsed JSON."""
    if not VERIFY_CITATIONS.exists():
        raise PackError(f"verify_citations.py not found at {VERIFY_CITATIONS}")
    cmd = [
        "/opt/homebrew/bin/python3",
        str(VERIFY_CITATIONS),
        str(document),
        "--extract-and-lookup-only",
        "-o",
        str(output),
    ]
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
    except subprocess.TimeoutExpired:
        raise PackError("verify_citations.py timed out (60s)")
    except FileNotFoundError as e:
        raise PackError(f"failed to launch verify_citations.py: {e}")
    if result.returncode != 0:
        raise PackError(
            f"verify_citations.py exited {result.returncode}: {result.stderr.strip()}"
        )
    try:
        return json.loads(output.read_text())
    except FileNotFoundError:
        raise PackError("verify_citations.py produced no output file")
    except json.JSONDecodeError as e:
        raise PackError(f"verify_citations.py output is not valid JSON: {e}")


def _validate_contract(data: dict) -> None:
    """Validate the extract-and-lookup-only JSON shape.

    Prevents mirror-unavailable being misreported as zero in-library coverage.
    """
    missing = REQUIRED_JSON_FIELDS - set(data.keys())
    if missing:
        raise PackError(f"extract JSON missing required fields: {sorted(missing)}")
    status = data.get("mirror_status")
    if status not in {"ready", "building", "stale", "unavailable"} and not isinstance(
        status, str
    ):
        raise PackError(f"unexpected mirror_status: {status!r}")
    if status != "ready" and not data.get("unavailable_reason"):
        # When the mirror is not ready, unavailable_reason MUST be populated so
        # the print line distinguishes 'no hits because nothing cited' from
        # 'no hits because mirror was unavailable'.
        raise PackError(
            f"mirror_status={status!r} but unavailable_reason is empty"
        )
    if not isinstance(data.get("hits"), list) or not isinstance(
        data.get("misses"), list
    ):
        raise PackError("hits/misses must be lists in extract JSON")


# -- Paper note section extraction --------------------------------------------

_H2_REGEX = re.compile(r"^##\s+(?!#)", re.MULTILINE)
_ABSTRACT_HEADING = re.compile(r"^##\s+Abstract\s*$", re.MULTILINE | re.IGNORECASE)
_HIGHLIGHTS_HEADING = re.compile(r"^##\s+Highlights\s*$", re.MULTILINE | re.IGNORECASE)
_HIGHLIGHT_LINE = re.compile(
    r"^>\s*p\.\s*(?P<page>\d+)\s*(?:\([^)]*\))?\s*[—-]\s*\*?(?P<text>.+?)\*?\s*$",
    re.IGNORECASE,
)


def _section_body(text: str, heading_regex: re.Pattern) -> str:
    """Return the body text under the FIRST matching H2 heading, up to the next H2."""
    m = heading_regex.search(text)
    if not m:
        return ""
    body_start = m.end()
    rest = text[body_start:]
    nxt = _H2_REGEX.search(rest)
    body = rest[: nxt.start()] if nxt else rest
    return body.strip()


def _truncate_words(body: str, cap: int) -> tuple[str, bool]:
    """Truncate body to `cap` words. Returns (truncated_text, was_truncated)."""
    words = body.split()
    if len(words) <= cap:
        return body, False
    return " ".join(words[:cap]), True


def _parse_highlights(body: str) -> list[dict]:
    """Parse `## Highlights` body into list of {page, text} dicts."""
    items: list[dict] = []
    for line in body.splitlines():
        line = line.strip()
        if not line.startswith(">"):
            continue
        m = _HIGHLIGHT_LINE.match(line)
        if m:
            items.append(
                {
                    "page": int(m.group("page")),
                    "text": m.group("text").strip(),
                }
            )
        else:
            # Non-conforming `>` line — keep raw text, no page sort key
            stripped = line.lstrip(">").strip()
            if stripped:
                items.append({"page": 10**9, "text": stripped})
    return items


# -- Author rendering ---------------------------------------------------------

def _render_authors(authors_resolved: list, fallback_authors_line: str) -> str:
    """Render the pack header's author string.

    Per spec §1b.3 / Codex L3 / Q11: 1-3 authors comma-separated, ≥4 → first
    et al. This is NOT identical to paper-note rendering (which uses first 3 +
    et al. + last for >5 authors).
    """
    names: list[str] = []
    for entry in authors_resolved or []:
        if isinstance(entry, dict):
            disp = entry.get("display") or entry.get("name")
            if disp:
                names.append(str(disp))
        elif isinstance(entry, str):
            names.append(entry)
    if not names and fallback_authors_line:
        # Fallback to the rendered **Authors:** line: strip wikilinks and *et al.*
        line = fallback_authors_line
        line = re.sub(r"\[\[[^\]]*\|([^\]]+)\]\]", r"\1", line)
        line = re.sub(r"\[\[([^\]]+)\]\]", r"\1", line)
        # Drop any "Full author list (N authors)" details block if present
        line = re.sub(r"<details>.*", "", line, flags=re.DOTALL)
        line = re.sub(r"\*et al\.\*", "et al.", line)
        return line.strip(" ,")
    if not names:
        return "Unknown authors"
    if len(names) >= 4:
        return f"{names[0]} et al."
    if len(names) == 3:
        return f"{names[0]}, {names[1]} & {names[2]}"
    if len(names) == 2:
        return f"{names[0]} & {names[1]}"
    return names[0]


def _first_author_surname(authors_resolved: list, fallback_authors_line: str) -> str:
    """Best-effort surname extraction for citation-frequency counting."""
    name = ""
    for entry in authors_resolved or []:
        if isinstance(entry, dict):
            disp = entry.get("display") or entry.get("name")
            if disp:
                name = str(disp)
                break
        elif isinstance(entry, str):
            name = entry
            break
    if not name and fallback_authors_line:
        m = re.search(r"\[\[[^\]]*\|([^\]]+)\]\]", fallback_authors_line)
        if m:
            name = m.group(1)
        else:
            m = re.match(r"^\*\*Authors:\*\*\s*([^\[,]+)", fallback_authors_line)
            if m:
                name = m.group(1).strip()
    surname = name.strip().split()[-1] if name.strip() else ""
    return surname


# -- Pack assembly ------------------------------------------------------------


def _read_paper_note(note_rel: str) -> tuple[Optional[dict], str, str]:
    """Read a paper note. Returns (frontmatter_dict | None, abstract_body, highlights_body)."""
    note_abs = VAULT_ROOT / note_rel
    if not note_abs.exists():
        return None, "", ""
    text = note_abs.read_text(encoding="utf-8")
    # Naive YAML frontmatter parse — pack only needs a handful of fields and
    # paper notes are generated by the mirror writer (well-formed by construction).
    fm: dict = {}
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            fm_text = text[4:end]
            for line in fm_text.splitlines():
                if ":" not in line or line.startswith(" "):
                    continue
                k, _, v = line.partition(":")
                fm[k.strip()] = v.strip().strip('"')
            text = text[end + 5:]
    # Pull the rendered **Authors:** line (first non-blank after frontmatter)
    fallback_authors = ""
    for line in text.splitlines():
        if line.startswith("**Authors:**"):
            fallback_authors = line
            break
    fm["_authors_line"] = fallback_authors
    abstract = _section_body(text, _ABSTRACT_HEADING)
    highlights = _section_body(text, _HIGHLIGHTS_HEADING)
    return fm, abstract, highlights


def _count_citation_frequency(doc_text: str, surname: str, year) -> int:
    """Count occurrences of `Surname...year` or `Surname et al. ... year` in the document.

    Loose heuristic — matches `Guerra (2017)`, `Guerra et al. 2017`, `Guerra, 2017`,
    `Guerra et al., 2017`. Returns at least 1 because the paper is by definition
    cited in the document (it's in the extracted DOI list).
    """
    if not surname or not year:
        return 1
    try:
        year_str = str(int(year))
    except (TypeError, ValueError):
        return 1
    safe_surname = re.escape(surname)
    pattern = re.compile(
        rf"\b{safe_surname}\b(?:\s+et\s+al\.?)?\s*[,(\s]+\s*{year_str}\b",
        re.IGNORECASE,
    )
    count = len(pattern.findall(doc_text))
    return max(count, 1)


def _resolve_authors(state_record: Optional[dict]) -> list:
    """Pull authors_resolved off the state-record hit. Caller may supplement
    with the paper-note's rendered Authors line if this is empty."""
    if not state_record:
        return []
    return state_record.get("authors_resolved") or []


def _adaptive_top_n(doc_word_count: int) -> int:
    return LONG_DOC_TOP_N if doc_word_count > LONG_DOC_WORD_THRESHOLD else DEFAULT_TOP_N


def _wikilink(note_rel: str, display: str) -> str:
    base = note_rel[:-3] if note_rel.endswith(".md") else note_rel
    return f"[[{base}|{display}]]"


def _format_entry(entry: dict) -> str:
    authors_label = entry["authors_label"]
    year = entry.get("year", "")
    journal = entry.get("journal", "")
    doi = entry.get("doi", "")
    wikilink = entry["wikilink"]
    labels = entry.get("paperpile_labels") or []
    labels_str = (
        " · Labels: " + ", ".join(str(l) for l in labels) if labels else ""
    )

    header = f"### {authors_label} ({year})"
    if journal:
        header += f" — *{journal}*"
    meta = f"DOI: {doi} · Paper note: {wikilink}{labels_str}"

    abstract = entry.get("abstract") or ""
    if abstract:
        abstract_trunc, was_trunc = _truncate_words(abstract, ABSTRACT_WORD_CAP)
        if was_trunc:
            abstract_trunc += " …[truncated]"
        abstract_block = f"**Abstract.** {abstract_trunc}"
    else:
        abstract_block = "**Abstract.** *(not available in paper note)*"

    highlights = entry.get("highlights") or []
    highlights = sorted(highlights, key=lambda h: h.get("page", 10**9))
    extra_count = max(0, len(highlights) - HIGHLIGHTS_PER_PAPER_CAP)
    capped = highlights[:HIGHLIGHTS_PER_PAPER_CAP]
    if capped:
        h_lines = []
        for h in capped:
            h_lines.append(f"> p. {h['page']} — *{h['text']}*")
        if extra_count:
            h_lines.append(f"(…{extra_count} more highlights in paper note)")
        highlights_block = "**Highlights.**\n" + "\n".join(h_lines)
    else:
        highlights_block = ""

    parts = [header, meta, "", abstract_block]
    if highlights_block:
        parts.append("")
        parts.append(highlights_block)
    return "\n".join(parts)


def build_pack(document: Path, output: Path) -> dict:
    """Build the curated literature pack. Returns a small dict describing what happened."""
    doc_text = document.read_text()
    doc_word_count = len(doc_text.split())

    with tempfile.NamedTemporaryFile(
        mode="w+", suffix=".json", delete=False
    ) as tf:
        extract_json_path = Path(tf.name)
    try:
        data = _run_verify_citations(document, extract_json_path)
        _validate_contract(data)
    finally:
        try:
            extract_json_path.unlink()
        except FileNotFoundError:
            pass

    mirror_status = data["mirror_status"]
    build_id = data.get("build_id") or "unknown"
    total = data.get("total_cited_dois") or 0
    extraction = data.get("extraction") or "headed"
    hits = data.get("hits") or []

    # If the mirror is unavailable, write a short "skipped" pack and return.
    if mirror_status != "ready":
        reason = data.get("unavailable_reason") or mirror_status
        pack = [
            "# Curated literature pack — Paperpile mirror",
            "",
            f"Pack unavailable: {reason}.",
            "",
            f"**Document under review:** {document}",
            "",
            (
                "/red-team Step 4b will still consult the Paperpile mirror for "
                "citation identity verification when the mirror becomes available."
            ),
        ]
        output.write_text("\n".join(pack))
        return {
            "skipped": True,
            "reason": reason,
            "mirror_status": mirror_status,
            "build_id": build_id,
            "in_library_count": 0,
            "total_cited_dois": total,
            "extraction": extraction,
            "capped_n": 0,
        }

    # Read paper notes and score for ranking
    rich_entries: list[dict] = []
    empty_entries: list[dict] = []
    for hit in hits:
        note_rel = hit.get("note_rel")
        if not note_rel:
            continue
        fm, abstract_body, highlights_body = _read_paper_note(note_rel)
        if fm is None:
            # Drift case: alias points at a slug whose note has disappeared
            continue
        highlights = _parse_highlights(highlights_body)
        authors_resolved = _resolve_authors(hit)
        if not authors_resolved:
            # Fallback: try to parse minimal authors from frontmatter `authors` field
            raw = fm.get("authors")
            if raw:
                raw_clean = raw.strip("[]")
                names = [n.strip().strip('"') for n in raw_clean.split(",") if n.strip()]
                authors_resolved = [{"display": n} for n in names]

        authors_label = _render_authors(authors_resolved, fm.get("_authors_line", ""))
        surname = _first_author_surname(authors_resolved, fm.get("_authors_line", ""))
        year = hit.get("year") or fm.get("year")
        cite_freq = _count_citation_frequency(doc_text, surname, year)

        journal = (
            hit.get("journal")
            or fm.get("journal")
            or fm.get("journal_full")
            or ""
        )
        labels = hit.get("paperpile_labels") or []
        title = hit.get("title") or fm.get("title") or ""

        wikilink_display = (
            f"{surname} {year}" if surname and year else (title[:60] or "paper note")
        )
        wikilink = _wikilink(note_rel, wikilink_display)

        entry = {
            "doi": hit.get("cited_doi"),
            "year": year,
            "journal": journal,
            "authors_label": authors_label,
            "surname": surname,
            "wikilink": wikilink,
            "paperpile_labels": labels,
            "abstract": abstract_body,
            "highlights": highlights,
            "title": title,
            "cite_freq": cite_freq,
            "abstract_word_count": len(abstract_body.split()) if abstract_body else 0,
            "highlights_count": len(highlights),
        }
        if not abstract_body and not highlights:
            empty_entries.append(entry)
        else:
            rich_entries.append(entry)

    cap = _adaptive_top_n(doc_word_count)

    def _rank_key(e):
        # Sort descending by: cite_freq, year, abstract_word_count, highlights_count
        try:
            year_int = int(e.get("year") or 0)
        except (TypeError, ValueError):
            year_int = 0
        return (
            -int(e.get("cite_freq", 1)),
            -year_int,
            -int(e.get("abstract_word_count", 0)),
            -int(e.get("highlights_count", 0)),
        )

    rich_entries.sort(key=_rank_key)
    capped = rich_entries[:cap]
    overflow = rich_entries[cap:]

    in_library_count = len(rich_entries) + len(empty_entries)
    pct = int(round(100 * in_library_count / total)) if total else 0

    parts: list[str] = []
    parts.append("# Curated literature pack — Paperpile mirror")
    parts.append("")
    parts.append(
        "This pack lists papers cited in the document being reviewed that Simon "
        "has in his curated Paperpile library. The abstracts and highlights below "
        "are extracted from his copies of these papers and represent the "
        "source-of-truth for what those papers actually said."
    )
    parts.append("")
    parts.append(
        f"**Coverage:** {in_library_count} of {total} cited DOIs resolved in-library "
        f"({pct}%)."
    )
    parts.append(
        f"**Pack policy:** Top {len(capped)} ranked by manuscript citation "
        "frequency, then year (recency), then abstract richness, then highlights "
        "count. Per-paper abstract truncated to ~250 words; max 3 highlights per "
        "paper. Remaining in-library hits listed in the footer without abstracts."
    )
    parts.append(f"**Build status:** {mirror_status} (build_id {build_id}).")
    parts.append(f"**References extraction:** {extraction}.")
    parts.append(f"**Document under review:** {document}")
    parts.append("")
    parts.append(
        "When evaluating any claim the manuscript makes about a paper in this "
        "pack, check it against the abstract and highlights below — these are "
        "the curated source of truth. **If the document contradicts the pack on "
        "a pack-listed paper, that is by default an error in the document, not "
        "the pack** (unless the pack itself is incomplete or ambiguous on the "
        "specific claim — in which case label your finding as *inference / "
        "needs verification*). Flag contradictions as High-severity Accuracy "
        "issues with specific quotes from both sides. For citations not in this "
        "pack, the external waterfall via Step 4b citation audit is the "
        "appropriate check — do not infer paper content from title, journal, or "
        "citation metadata alone."
    )
    parts.append("")

    if not capped and not empty_entries and not overflow:
        parts.append("*(No in-library hits among the cited references.)*")
    else:
        for entry in capped:
            parts.append(_format_entry(entry))
            parts.append("")

        footer_items = overflow + empty_entries
        if footer_items:
            parts.append("---")
            parts.append("")
            parts.append(
                "## Also cited and in library — abstracts/highlights omitted"
            )
            parts.append("")
            for entry in footer_items:
                year_str = f" ({entry['year']})" if entry.get("year") else ""
                parts.append(f"- {entry['wikilink']}{year_str}")

    output.write_text("\n".join(parts) + "\n")

    return {
        "skipped": False,
        "reason": None,
        "mirror_status": mirror_status,
        "build_id": build_id,
        "in_library_count": in_library_count,
        "total_cited_dois": total,
        "extraction": extraction,
        "capped_n": len(capped),
    }


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Build the /red-team Paperpile curated-literature pack for a document"
        )
    )
    parser.add_argument("document", help="Path to the document under review")
    parser.add_argument(
        "-o",
        "--output",
        default=str(DEFAULT_OUTPUT),
        help=f"Pack output path (default: {DEFAULT_OUTPUT})",
    )
    args = parser.parse_args()
    doc = Path(args.document)
    if not doc.exists():
        print(f"Document not found: {doc}", file=sys.stderr)
        sys.exit(1)
    output = Path(args.output)
    try:
        result = build_pack(doc, output)
    except PackError as e:
        print(f"[1b] Paperpile pack — skipped ({e})", file=sys.stderr)
        sys.exit(0)
    if result["skipped"]:
        print(
            f"[1b] Paperpile pack — skipped (mirror unavailable: {result['reason']})",
            file=sys.stderr,
        )
        return
    total = result["total_cited_dois"]
    in_lib = result["in_library_count"]
    pct = int(round(100 * in_lib / total)) if total else 0
    print(
        f"[1b] Paperpile pack — {in_lib}/{total} cited DOIs in-library ({pct}%), "
        f"top {result['capped_n']} in pack (build_id {result['build_id']}, "
        f"references_extraction: {result['extraction']})",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
