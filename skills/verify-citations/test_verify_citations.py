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
