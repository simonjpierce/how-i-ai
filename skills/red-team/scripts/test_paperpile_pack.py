"""Unit tests for paperpile_pack.py — the /red-team Step 1b pack builder.

Covers JSON contract validation, paper-note section extraction, author
rendering, citation-frequency counting, adaptive top-N cap, ranking,
and pack-skip semantics. Pack builds for live mirror state are exercised
via the production smoke-test path (driven from /red-team), not from pytest.

Run: /opt/homebrew/bin/python3 -m pytest -v test_paperpile_pack.py
"""

import importlib.util
import json
import sys
from pathlib import Path

import pytest

SKILL_DIR = Path(__file__).parent
sys.path.insert(0, str(SKILL_DIR))

spec = importlib.util.spec_from_file_location(
    "paperpile_pack", SKILL_DIR / "paperpile_pack.py"
)
pp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pp)


# ---- JSON contract validation -----------------------------------------------


def test_validate_contract_accepts_ready_payload():
    pp._validate_contract(
        {
            "document": "/tmp/x.md",
            "extraction": "headed",
            "mirror_status": "ready",
            "build_id": "abc",
            "unavailable_reason": None,
            "total_cited_dois": 3,
            "hits": [],
            "misses": [],
        }
    )  # No exception


def test_validate_contract_accepts_unavailable_with_reason():
    pp._validate_contract(
        {
            "document": "/tmp/x.md",
            "extraction": "headed",
            "mirror_status": "building",
            "build_id": None,
            "unavailable_reason": "build-status: 'building'",
            "total_cited_dois": 0,
            "hits": [],
            "misses": [],
        }
    )


def test_validate_contract_rejects_missing_field():
    with pytest.raises(pp.PackError, match="missing"):
        pp._validate_contract({"mirror_status": "ready"})


def test_validate_contract_rejects_unavailable_without_reason():
    """Codex M4 — mirror_status != ready MUST carry an unavailable_reason."""
    with pytest.raises(pp.PackError, match="unavailable_reason is empty"):
        pp._validate_contract(
            {
                "document": "/tmp/x.md",
                "extraction": "headed",
                "mirror_status": "building",
                "build_id": None,
                "unavailable_reason": None,
                "total_cited_dois": 0,
                "hits": [],
                "misses": [],
            }
        )


def test_validate_contract_rejects_non_list_hits():
    with pytest.raises(pp.PackError, match="lists"):
        pp._validate_contract(
            {
                "document": "/tmp/x.md",
                "extraction": "headed",
                "mirror_status": "ready",
                "build_id": "abc",
                "unavailable_reason": None,
                "total_cited_dois": 0,
                "hits": "not a list",
                "misses": [],
            }
        )


# ---- Adaptive top-N cap -----------------------------------------------------


def test_adaptive_top_n_short_doc():
    assert pp._adaptive_top_n(2000) == pp.DEFAULT_TOP_N == 20


def test_adaptive_top_n_long_doc():
    """Document >8000 words drops top-N to 10 (matches red-team SKILL.md:47 flag)."""
    assert pp._adaptive_top_n(8001) == pp.LONG_DOC_TOP_N == 10


def test_adaptive_top_n_at_threshold():
    """Exactly at the threshold counts as short."""
    assert pp._adaptive_top_n(8000) == pp.DEFAULT_TOP_N


# ---- Paper-note section extraction ------------------------------------------


def test_section_body_abstract():
    text = (
        "**Authors:** A B\n\n"
        "## Abstract\n\n"
        "This is the abstract paragraph.\n\n"
        "## Highlights\n\n"
        "> p. 1 — *foo*\n"
    )
    body = pp._section_body(text, pp._ABSTRACT_HEADING)
    assert "This is the abstract paragraph." in body
    assert ">" not in body  # Highlights section excluded


def test_section_body_highlights():
    text = (
        "## Abstract\n\nAbs.\n\n"
        "## Highlights\n\n"
        "> p. 1 — *first*\n"
        "> p. 3 — *third*\n\n"
        "## References in library\n\n"
        "*(empty)*\n"
    )
    body = pp._section_body(text, pp._HIGHLIGHTS_HEADING)
    assert "first" in body
    assert "third" in body
    assert "References in library" not in body


def test_section_body_missing_returns_empty():
    text = "## Abstract\n\nNo highlights section here.\n"
    body = pp._section_body(text, pp._HIGHLIGHTS_HEADING)
    assert body == ""


# ---- Highlights parsing -----------------------------------------------------


def test_parse_highlights_simple():
    body = (
        "> p. 8 (Yellow, 2026-05-12T21:42:37+12:00) — *Foraging dives mean 50 min*\n"
        "> p. 9 (Yellow, 2026-05-12T21:43:00+12:00) — *Max depth 1439 m*\n"
    )
    items = pp._parse_highlights(body)
    assert len(items) == 2
    assert items[0]["page"] == 8
    assert "Foraging" in items[0]["text"]


def test_parse_highlights_empty_body():
    assert pp._parse_highlights("") == []


def test_parse_highlights_ignores_non_quote_lines():
    body = "Some intro text.\n> p. 1 — *real highlight*\nMore text.\n"
    items = pp._parse_highlights(body)
    assert len(items) == 1
    assert "real highlight" in items[0]["text"]


# ---- Word truncation --------------------------------------------------------


def test_truncate_words_under_cap():
    text = "one two three"
    truncated, was_trunc = pp._truncate_words(text, 5)
    assert truncated == text
    assert was_trunc is False


def test_truncate_words_over_cap():
    text = " ".join(f"w{i}" for i in range(300))
    truncated, was_trunc = pp._truncate_words(text, 250)
    assert was_trunc is True
    assert len(truncated.split()) == 250


# ---- Author rendering -------------------------------------------------------


def test_render_authors_single():
    out = pp._render_authors([{"display": "Marta Guerra"}], "")
    assert out == "Marta Guerra"


def test_render_authors_two():
    out = pp._render_authors(
        [{"display": "A B"}, {"display": "C D"}], ""
    )
    assert out == "A B & C D"


def test_render_authors_three():
    out = pp._render_authors(
        [{"display": "A B"}, {"display": "C D"}, {"display": "E F"}], ""
    )
    assert "A B, C D & E F" == out


def test_render_authors_four_uses_et_al():
    """Codex L3 / Q11 — pack uses simple et al. for >=4 authors, NOT the
    paper-note rendering (first 3 + et al. + last)."""
    authors = [{"display": f"Author {i}"} for i in range(4)]
    out = pp._render_authors(authors, "")
    assert out == "Author 0 et al."


def test_render_authors_seven_uses_simple_et_al():
    """For 7 authors, pack still uses simple `first et al.` (not
    paper-note's `first 3 + et al. + last`)."""
    authors = [{"display": f"Author {i}"} for i in range(7)]
    out = pp._render_authors(authors, "")
    assert out == "Author 0 et al."


def test_render_authors_empty_resolved_uses_fallback():
    fallback = (
        "**Authors:** [[some/path|Marta Guerra]], [[other/path|Leigh Hickmott]] "
        "*et al.*, [[end/path|Michael Moore]]"
    )
    out = pp._render_authors([], fallback)
    assert "Marta Guerra" in out
    assert "[[" not in out  # wikilinks stripped


def test_render_authors_empty_both_returns_unknown():
    assert pp._render_authors([], "") == "Unknown authors"


# ---- Citation frequency counting --------------------------------------------


def test_cite_freq_counts_in_text_citation():
    doc = (
        "Guerra (2017) reported foraging depths. Guerra et al. (2017) extended "
        "this. The Guerra 2017 paper also notes prey distribution."
    )
    assert pp._count_citation_frequency(doc, "Guerra", 2017) == 3


def test_cite_freq_returns_at_least_one():
    """Even when no in-text match, paper is by definition cited (DOI in refs)."""
    doc = "No mention of any names in this body."
    assert pp._count_citation_frequency(doc, "Guerra", 2017) == 1


def test_cite_freq_uppercase_et_al():
    doc = "Guerra et al. 2017 demonstrate..."
    assert pp._count_citation_frequency(doc, "Guerra", 2017) == 1


def test_cite_freq_handles_missing_surname():
    doc = "Body text."
    assert pp._count_citation_frequency(doc, "", 2017) == 1


# ---- Pack header: mirror unavailable writes skipped pack --------------------


def test_build_pack_writes_unavailable_pack(tmp_path, monkeypatch):
    """When extract-and-lookup-only reports mirror_status != 'ready', the pack
    builder writes a short 'unavailable' pack and returns skipped=True."""

    extract_json = {
        "document": "/tmp/x.md",
        "extraction": "headed",
        "mirror_status": "building",
        "build_id": None,
        "unavailable_reason": "build-status: 'building'",
        "total_cited_dois": 0,
        "hits": [],
        "misses": [],
    }

    def fake_run(document, output):
        return extract_json

    monkeypatch.setattr(pp, "_run_verify_citations", fake_run)
    doc = tmp_path / "doc.md"
    doc.write_text("# Doc\n\n## References\n\nGuerra (2017) X. 10.x/y.\n")
    out = tmp_path / "pack.md"
    result = pp.build_pack(doc, out)
    assert result["skipped"] is True
    assert result["mirror_status"] == "building"
    pack_text = out.read_text()
    assert "Pack unavailable" in pack_text
    assert "building" in pack_text


# ---- Pack ranking by citation frequency (Codex UR5/Q12) ---------------------


def test_pack_ranks_by_citation_frequency(tmp_path, monkeypatch):
    """Codex UR5/Q12 — primary key is manuscript citation frequency. A heavily
    cited older paper outranks a recently published once-cited paper."""

    # Two paper notes — write to a temp papers dir matching the vault layout.
    # Use realistic surnames so _first_author_surname picks the surname correctly.
    papers_root = tmp_path / "Paperpile Library" / "papers"
    papers_root.mkdir(parents=True)
    paper_a_path = papers_root / "guerrini-2010-frequent.md"
    paper_a_path.write_text(
        "---\ntype: paper\nauthors: [Guerrini]\nyear: 2010\n---\n"
        "**Authors:** [[some/Guerrini|Guerrini]]\n\n"
        "## Abstract\n\nShort abstract for the frequent paper.\n\n"
        "## Highlights\n\n*(empty)*\n"
    )
    paper_b_path = papers_root / "novak-2024-rare.md"
    paper_b_path.write_text(
        "---\ntype: paper\nauthors: [Novak]\nyear: 2024\n---\n"
        "**Authors:** [[some/Novak|Novak]]\n\n"
        "## Abstract\n\nA longer abstract with many more words than the other "
        "paper covers in its short summary. This one has a richer abstract "
        "and is more recent.\n\n"
        "## Highlights\n\n> p. 1 — *one*\n> p. 2 — *two*\n> p. 3 — *three*\n"
    )

    # Document body cites Guerrini 5 times, Novak once
    doc = tmp_path / "doc.md"
    doc_text = (
        "Body. Guerrini (2010) said X. Guerrini et al. 2010 confirmed. Guerrini 2010 also.\n"
        "Guerrini (2010) repeats. Guerrini 2010 again. Novak (2024) noted Y.\n\n"
        "## References\n\n"
        "Guerrini (2010) X. 10.9999/alpha.\n\n"
        "Novak (2024) Y. 10.9999/beta.\n"
    )
    doc.write_text(doc_text)

    extract_json = {
        "document": str(doc),
        "extraction": "headed",
        "mirror_status": "ready",
        "build_id": "fixture-001",
        "unavailable_reason": None,
        "total_cited_dois": 2,
        "hits": [
            {
                "cited_doi": "10.9999/alpha",
                "pub_id": "p1",
                "note_rel": str(paper_a_path.relative_to(tmp_path)),
                "year": 2010,
                "title": "Guerrini title",
                "journal": "J Frequent",
                "slug": "guerrini-2010-frequent",
                "paperpile_labels": [],
                "has_abstract": True,
                "has_highlights": False,
            },
            {
                "cited_doi": "10.9999/beta",
                "pub_id": "p2",
                "note_rel": str(paper_b_path.relative_to(tmp_path)),
                "year": 2024,
                "title": "Novak title",
                "journal": "J Rare",
                "slug": "novak-2024-rare",
                "paperpile_labels": [],
                "has_abstract": True,
                "has_highlights": True,
            },
        ],
        "misses": [],
    }

    def fake_run(document, output):
        return extract_json

    # Re-root VAULT_ROOT so note_rel paths resolve under tmp_path
    monkeypatch.setattr(pp, "VAULT_ROOT", tmp_path)
    monkeypatch.setattr(pp, "_run_verify_citations", fake_run)

    out = tmp_path / "pack.md"
    result = pp.build_pack(doc, out)
    assert result["skipped"] is False
    pack_text = out.read_text()

    # Guerrini must appear before Novak — higher citation frequency
    g_idx = pack_text.index("Guerrini")
    n_idx = pack_text.index("Novak")
    assert g_idx < n_idx, (
        f"Guerrini (5 citations, 2010) should rank above Novak (1 citation, 2024) "
        f"— citation frequency is primary key. Got Guerrini at {g_idx}, Novak at {n_idx}"
    )


# ---- Adaptive cap fires on long documents (test 25) ------------------------


def test_pack_cap_drops_for_long_docs(tmp_path, monkeypatch):
    """Doc word count >8000 triggers adaptive cap of 10 (down from 20)."""

    papers_root = tmp_path / "papers"
    papers_root.mkdir(parents=True)
    hits = []
    for i in range(15):
        note = papers_root / f"author{i}-2020-p{i}.md"
        note.write_text(
            f"---\ntype: paper\nauthors: [Author {i}]\nyear: 2020\n---\n"
            f"**Authors:** [[some/Author {i}|Author {i}]]\n\n"
            f"## Abstract\n\nAbstract for paper {i}.\n\n## Highlights\n\n"
        )
        hits.append(
            {
                "cited_doi": f"10.9999/p{i}",
                "pub_id": f"pid{i}",
                "note_rel": str(note.relative_to(tmp_path)),
                "year": 2020,
                "title": f"Title {i}",
                "journal": "J",
                "slug": f"author{i}-2020-p{i}",
                "paperpile_labels": [],
                "has_abstract": True,
                "has_highlights": False,
            }
        )

    long_body = " ".join(f"word{i}" for i in range(9000))
    doc = tmp_path / "long-doc.md"
    doc.write_text(f"# Doc\n\n{long_body}\n\n## References\n\nAuthor 0 (2020) etc.\n")

    extract_json = {
        "document": str(doc),
        "extraction": "headed",
        "mirror_status": "ready",
        "build_id": "fixture-long",
        "unavailable_reason": None,
        "total_cited_dois": 15,
        "hits": hits,
        "misses": [],
    }

    monkeypatch.setattr(pp, "VAULT_ROOT", tmp_path)
    monkeypatch.setattr(pp, "_run_verify_citations", lambda d, o: extract_json)
    out = tmp_path / "pack.md"
    result = pp.build_pack(doc, out)
    assert result["capped_n"] == pp.LONG_DOC_TOP_N == 10
    pack_text = out.read_text()
    # Confirm the footer mentions papers that didn't fit
    assert "Also cited and in library" in pack_text
