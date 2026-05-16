"""Unit tests for verify_citations.py — covers the Paperpile integration.

Focuses on the pure helpers (DOI normalisation, regex extraction, source-of-
truth validation). The mirror loader is tested via stubbing the module-level
state to avoid touching the live 190MB state.json on every test run.

Run: /opt/homebrew/bin/python3 -m pytest -v test_verify_citations.py
"""

import importlib.util
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).parent
sys.path.insert(0, str(SKILL_DIR))

spec = importlib.util.spec_from_file_location(
    "verify_citations", SKILL_DIR / "verify_citations.py"
)
vc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vc)


# ---- DOI normalisation -------------------------------------------------------


def test_normalise_lowercases():
    assert vc._normalise_doi("10.6620/ZS.2025.64-01") == "10.6620/zs.2025.64-01"


def test_normalise_strips_https_prefix():
    assert (
        vc._normalise_doi("https://doi.org/10.1016/j.dsr.2017.08.012")
        == "10.1016/j.dsr.2017.08.012"
    )


def test_normalise_strips_http_prefix():
    assert (
        vc._normalise_doi("http://doi.org/10.1016/j.dsr.2017.08.012")
        == "10.1016/j.dsr.2017.08.012"
    )


def test_normalise_strips_dx_doi_prefix():
    assert (
        vc._normalise_doi("https://dx.doi.org/10.1016/j.dsr.2017.08.012")
        == "10.1016/j.dsr.2017.08.012"
    )


def test_normalise_strips_doi_colon_prefix():
    assert vc._normalise_doi("doi: 10.1016/j.dsr.2017.08.012") == "10.1016/j.dsr.2017.08.012"


def test_normalise_strips_uppercase_DOI_prefix():
    assert vc._normalise_doi("DOI: 10.1016/j.dsr.2017.08.012") == "10.1016/j.dsr.2017.08.012"


def test_normalise_strips_trailing_punctuation():
    assert vc._normalise_doi("10.1016/j.dsr.2017.08.012.") == "10.1016/j.dsr.2017.08.012"
    assert vc._normalise_doi("10.1016/j.dsr.2017.08.012,") == "10.1016/j.dsr.2017.08.012"
    assert vc._normalise_doi("10.1016/j.dsr.2017.08.012)") == "10.1016/j.dsr.2017.08.012"


def test_normalise_empty():
    assert vc._normalise_doi("") == ""
    assert vc._normalise_doi(None) == ""


# ---- DOI regex extraction ---------------------------------------------------


def test_extract_bare_doi():
    ref = "Guerra (2017) Diverse foraging strategies. Deep-Sea Res 10.1016/j.dsr.2017.08.012"
    assert vc._extract_doi(ref) == "10.1016/j.dsr.2017.08.012"


def test_extract_doi_with_url_prefix():
    ref = "Guerra (2017) Diverse foraging. https://doi.org/10.1016/j.dsr.2017.08.012"
    assert vc._extract_doi(ref) == "10.1016/j.dsr.2017.08.012"


def test_extract_doi_with_doi_colon_prefix():
    ref = "Guerra (2017) Diverse foraging. doi: 10.1016/j.dsr.2017.08.012"
    assert vc._extract_doi(ref) == "10.1016/j.dsr.2017.08.012"


def test_extract_sici_style_doi():
    """Codex MC4 — angle brackets in SICI-style DOIs must NOT truncate the suffix."""
    ref = "Foo (1994) Title. Trans Am Fish Soc 10.1577/1548-8659(1994)123<0242:aageft>2.3.co;2"
    extracted = vc._extract_doi(ref)
    assert "<0242:aageft>" in extracted, f"SICI truncated: got {extracted!r}"


def test_extract_markdown_wrapped_doi():
    ref = "Guerra (2017) Diverse foraging. [Guerra 2017](https://doi.org/10.1016/j.dsr.2017.08.012)"
    assert vc._extract_doi(ref) == "10.1016/j.dsr.2017.08.012"


def test_extract_no_doi():
    assert vc._extract_doi("Guerra (2017) Diverse foraging. Deep-Sea Res 132:10-20.") is None


# ---- parse_reference populates doi ------------------------------------------


def test_parse_reference_populates_doi():
    ref = (
        "Guerra M (2017) Diverse foraging strategies by a marine top predator. "
        "Deep-Sea Res 132:10-20. https://doi.org/10.1016/j.dsr.2017.08.012"
    )
    parsed = vc.parse_reference(ref)
    assert parsed["doi"] == "10.1016/j.dsr.2017.08.012"
    assert parsed["year"] == 2017
    assert parsed["first_author"].lower().startswith("guerra")


# ---- lookup_in_paperpile drift-handling ------------------------------------


def _stub_mirror(monkeypatch, state, doi_index):
    monkeypatch.setattr(vc, "_MIRROR_AVAILABILITY", True)
    monkeypatch.setattr(vc, "_MIRROR_STATE", state)
    monkeypatch.setattr(vc, "_MIRROR_DOI_INDEX", doi_index)
    monkeypatch.setattr(vc, "_MIRROR_DISABLED", False)


def test_lookup_hit(monkeypatch, tmp_path):
    # Build a note file the existence check expects
    papers_dir = vc.VAULT_ROOT / "02_MARINE MEGAFAUNA" / "REFERENCE LIBRARY" / "Paperpile Library" / "papers"
    note = papers_dir / "guerra-2017-diverse-foraging-strategies-marine-top-predator.md"
    # Don't create — assume the real one exists; this test verifies the lookup
    # plumbing against the real on-disk note file.
    state = {
        "paper_records": {
            "pid": {
                "pub_id": "pid",
                "slug": "guerra-2017-diverse-foraging-strategies-marine-top-predator",
                "doi": "10.1016/j.dsr.2017.08.012",
                "year": 2017,
                "title": "Diverse foraging strategies",
                "authors_resolved": [{"display": "Marta Guerra"}],
            }
        },
    }
    _stub_mirror(monkeypatch, state, {"10.1016/j.dsr.2017.08.012": "pid"})
    rec, rel = vc.lookup_in_paperpile("10.1016/j.dsr.2017.08.012")
    if note.exists():
        assert rec is not None
        assert rel.endswith("guerra-2017-diverse-foraging-strategies-marine-top-predator.md")
    else:
        # If the actual note isn't present we expect fall-through to None
        assert rec is None


def test_lookup_stale_alias_to_missing_pub_id(monkeypatch):
    state = {"paper_records": {}}
    _stub_mirror(monkeypatch, state, {"10.999/stale": "missing-pub-id"})
    rec, rel = vc.lookup_in_paperpile("10.999/stale")
    assert rec is None and rel is None


def test_lookup_doi_drift(monkeypatch):
    """Alias maps to a record whose stored DOI no longer matches — fall through."""
    state = {
        "paper_records": {
            "pid": {
                "pub_id": "pid",
                "slug": "some-slug",
                "doi": "10.999/corrected",
                "authors_resolved": [],
            }
        }
    }
    _stub_mirror(monkeypatch, state, {"10.999/old": "pid"})
    rec, rel = vc.lookup_in_paperpile("10.999/old")
    assert rec is None and rel is None


def test_lookup_missing_slug(monkeypatch):
    state = {
        "paper_records": {
            "pid": {"pub_id": "pid", "doi": "10.999/x", "authors_resolved": []}
        }
    }
    _stub_mirror(monkeypatch, state, {"10.999/x": "pid"})
    rec, rel = vc.lookup_in_paperpile("10.999/x")
    assert rec is None and rel is None


def test_lookup_disabled(monkeypatch):
    monkeypatch.setattr(vc, "_MIRROR_DISABLED", True)
    monkeypatch.setattr(vc, "_MIRROR_AVAILABILITY", False)
    rec, rel = vc.lookup_in_paperpile("10.1016/j.dsr.2017.08.012")
    assert rec is None and rel is None


# ---- _check_inlibrary_consistency ------------------------------------------


def test_consistency_clean():
    parsed = {"first_author": "Guerra", "year": 2017}
    record = {
        "year": 2017,
        "authors_resolved": [{"display": "Marta Guerra"}],
    }
    issues = vc._check_inlibrary_consistency(parsed, record)
    assert issues == []


def test_consistency_year_mismatch():
    parsed = {"first_author": "Guerra", "year": 2019}
    record = {
        "year": 2017,
        "authors_resolved": [{"display": "Marta Guerra"}],
    }
    issues = vc._check_inlibrary_consistency(parsed, record)
    assert any("Year mismatch" in i for i in issues)


def test_consistency_year_within_one_year_ok():
    parsed = {"first_author": "Guerra", "year": 2018}
    record = {
        "year": 2017,
        "authors_resolved": [{"display": "Marta Guerra"}],
    }
    issues = vc._check_inlibrary_consistency(parsed, record)
    assert issues == []


def test_consistency_author_mismatch():
    parsed = {"first_author": "Smith", "year": 2017}
    record = {
        "year": 2017,
        "authors_resolved": [{"display": "Marta Guerra"}],
    }
    issues = vc._check_inlibrary_consistency(parsed, record)
    assert any("First author mismatch" in i for i in issues)


def test_consistency_empty_authors_skips_silently():
    parsed = {"first_author": "Anyone", "year": 2017}
    record = {"year": 2017, "authors_resolved": []}
    issues = vc._check_inlibrary_consistency(parsed, record)
    assert issues == []  # No author info in record → skip the check


# ---- Argparse flag wiring (smoke) -------------------------------------------


def test_set_paperpile_disabled():
    vc.set_paperpile_disabled(True)
    assert vc._MIRROR_AVAILABILITY is False
    assert vc._MIRROR_DISABLED is True
    # Reset for any subsequent tests
    vc.set_paperpile_disabled(False)
    vc._MIRROR_AVAILABILITY = None


# ---- Broadened references-section heading variants (Codex 2026-05-16) ---------


def test_extract_references_matches_sources_heading():
    """Broadened pattern catches `## Sources` (vault: Strategic Plan Review)."""
    text = (
        "# Intro\n\nBody.\n\n"
        "## Sources\n\n"
        "Guerra M (2017) Diverse foraging. Deep-Sea Res 10.1016/j.dsr.2017.08.012.\n"
    )
    refs = vc.extract_references(text)
    assert len(refs) == 1
    assert "Guerra" in refs[0]


def test_extract_references_matches_reference_list_heading():
    text = (
        "# Intro\n\n## Reference List\n\n"
        "Smith J (2024) Title here. Journal of Things 10.9999/test.\n"
    )
    refs = vc.extract_references(text)
    assert len(refs) == 1


def test_extract_references_matches_references_cited_heading():
    text = (
        "## References Cited\n\n"
        "Jones K (2020) A paper. Mar Bio 10.9999/jones.\n"
    )
    refs = vc.extract_references(text)
    assert len(refs) == 1


def test_extract_references_matches_cited_works_heading():
    text = (
        "## Cited Works\n\n"
        "Brown M (2019) Another paper. Sci 10.9999/brown.\n"
    )
    refs = vc.extract_references(text)
    assert len(refs) == 1


def test_extract_references_matches_references_with_suffix():
    """References (draft) — suffix-tolerant via `[\\w\\s]*References?` prefix."""
    text = (
        "## References (draft / incomplete)\n\n"
        "Lee P (2018) Suffix test. Bio 10.9999/lee.\n"
    )
    refs = vc.extract_references(text)
    assert len(refs) == 1


def test_extract_references_works_cited():
    text = (
        "## Works Cited\n\n"
        "Ng A (2023) Title. AI 10.9999/ng.\n"
    )
    refs = vc.extract_references(text)
    assert len(refs) == 1


# ---- extract_cited_dois_from_document --------------------------------------


def test_extract_cited_dois_headed_section():
    text = (
        "# Manuscript\n\nBody text.\n\n"
        "## References\n\n"
        "Guerra M (2017) Title. Deep-Sea Res 10.1016/j.dsr.2017.08.012.\n\n"
        "Smith J (2024) Other. Bio 10.9999/smith.\n"
    )
    dois, extraction = vc.extract_cited_dois_from_document(text)
    assert extraction == "headed"
    assert "10.1016/j.dsr.2017.08.012" in dois
    assert "10.9999/smith" in dois


def test_extract_cited_dois_multiple_sections():
    """Multi-section bibliography: ## References + ## Sources both contribute DOIs."""
    text = (
        "## References\n\n"
        "Guerra M (2017) Title. Deep-Sea Res 10.1016/j.dsr.2017.08.012.\n\n"
        "## Sources\n\n"
        "Smith J (2024) Other. Bio 10.9999/smith.\n"
    )
    dois, extraction = vc.extract_cited_dois_from_document(text)
    assert extraction == "headed"
    assert "10.1016/j.dsr.2017.08.012" in dois
    assert "10.9999/smith" in dois


def test_extract_cited_dois_full_document_fallback():
    """No References section → fall back to whole-document DOI scan."""
    text = (
        "# Blog post\n\nSee Guerra 2017 (https://doi.org/10.1016/j.dsr.2017.08.012) "
        "for foraging data. Also Smith 2024 (doi:10.9999/smith).\n"
    )
    dois, extraction = vc.extract_cited_dois_from_document(text)
    assert extraction == "full_document_fallback"
    assert "10.1016/j.dsr.2017.08.012" in dois
    assert "10.9999/smith" in dois


def test_extract_cited_dois_dedup():
    text = (
        "## References\n\n"
        "Guerra M (2017) A. 10.1016/j.dsr.2017.08.012.\n\n"
        "Guerra M (2017) A (reprint). 10.1016/j.dsr.2017.08.012.\n"
    )
    dois, _ = vc.extract_cited_dois_from_document(text)
    assert dois.count("10.1016/j.dsr.2017.08.012") == 1


def test_extract_cited_dois_uses_finditer_not_extract_doi():
    """Codex H1 — full-document fallback MUST use finditer, not _extract_doi
    (which returns only the first match). Five DOIs in body, all must appear."""
    text = "\n".join(
        f"Paper {i}: 10.9999/p{i}" for i in range(5)
    )
    dois, extraction = vc.extract_cited_dois_from_document(text)
    assert extraction == "full_document_fallback"
    assert len(dois) == 5, f"expected 5 DOIs, got {dois}"


def test_extract_cited_dois_no_dois_anywhere():
    text = "# No DOIs here\n\nJust prose body content. No references section.\n"
    dois, extraction = vc.extract_cited_dois_from_document(text)
    assert dois == []
    assert extraction == "full_document_fallback"


def test_extract_cited_dois_order_of_first_appearance():
    """DOI order is preserved by first appearance for stable pack ordering."""
    text = (
        "## References\n\n"
        "B (2020) Paper. 10.9999/bbb.\n\n"
        "A (2018) Paper. 10.9999/aaa.\n\n"
        "C (2024) Paper. 10.9999/ccc.\n"
    )
    dois, _ = vc.extract_cited_dois_from_document(text)
    assert dois == ["10.9999/bbb", "10.9999/aaa", "10.9999/ccc"]


# ---- _mirror_metadata (fixture-backed) -------------------------------------


def test_mirror_metadata_ready(monkeypatch):
    """When mirror is stubbed available, metadata reports ready."""
    monkeypatch.setattr(vc, "_MIRROR_DISABLED", False)
    monkeypatch.setattr(vc, "_MIRROR_AVAILABILITY", True)
    monkeypatch.setattr(vc, "_MIRROR_STATE", {"paper_records": {}, "aliases": {"doi": {}}})
    monkeypatch.setattr(vc, "_MIRROR_DOI_INDEX", {})

    # Build-status file: build-status path is read at runtime; stub via tmp file
    import tempfile, json as _json
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tf:
        tf.write(_json.dumps({"status": "ready", "build_id": "fixture-001"}))
        tf_path = tf.name
    from pathlib import Path as _P
    monkeypatch.setattr(vc, "PAPERPILE_BUILD_STATUS", _P(tf_path))

    status, build_id, reason = vc._mirror_metadata()
    assert status == "ready"
    assert build_id == "fixture-001"
    assert reason is None


def test_mirror_metadata_missing_build_status(monkeypatch, tmp_path):
    """Build-status file missing → unavailable with reason."""
    monkeypatch.setattr(vc, "_MIRROR_DISABLED", False)
    monkeypatch.setattr(vc, "PAPERPILE_BUILD_STATUS", tmp_path / "nonexistent")
    status, build_id, reason = vc._mirror_metadata()
    assert status == "unavailable"
    assert build_id is None
    assert reason and "missing" in reason


def test_mirror_metadata_building(monkeypatch, tmp_path):
    """Status reports building → propagated as 'building' with reason."""
    monkeypatch.setattr(vc, "_MIRROR_DISABLED", False)
    bs_path = tmp_path / "build-status"
    bs_path.write_text('{"status": "building", "build_id": "fixture-002"}')
    monkeypatch.setattr(vc, "PAPERPILE_BUILD_STATUS", bs_path)
    status, build_id, reason = vc._mirror_metadata()
    assert status == "building"
    assert build_id == "fixture-002"
    assert reason and "building" in reason


def test_mirror_metadata_disabled(monkeypatch):
    """--no-paperpile sets disabled → metadata reports unavailable."""
    monkeypatch.setattr(vc, "_MIRROR_DISABLED", True)
    status, build_id, reason = vc._mirror_metadata()
    assert status == "unavailable"
    assert reason and "disabled" in reason


# ---- CONFLICT report wording uses 'identity' not 'representation' -----------


def test_report_conflict_wording_identity():
    """Codex 2026-05-16 — fix wording so Step 4b says 'identity' (not 'representation'),
    preserving the distinction with /red-team Step 1b which DOES check representation."""
    results = [
        {
            "reference": "Guerra (2017) X. 10.x/y",
            "first_author": "Guerra",
            "year": 2017,
            "title_query": "X",
            "status": "CONFLICT",
            "issues": ["Year mismatch: ref=2017, found=2019"],
            "doi": "10.x/y",
            "matched_title": "X",
            "source_api": "Paperpile (in-library)",
            "paperpile_note": "papers/test.md",
            "paperpile_pub_id": "pid",
        }
    ]
    report = vc.format_report(results, "test.md")
    assert "identity disagrees" in report or "author/year identity" in report
    assert "Step 1b" in report or "curated literature pack" in report
