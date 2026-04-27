# Domain Routing

Detect the query domain during scoping and use it to guide source selection in Phase 3.

## Domain table

| Domain | Primary sources | Notes |
|--------|----------------|-------|
| **Marine biology / conservation** | Peer-reviewed literature, IUCN, NGO reports | Check vault expedition notes and fact files first |
| **Photography / gear** | Gear reviews, manufacturer specs | No programmatic APIs for gear retailers |
| **Non-profit operations** | Bridgespan, SSIR, InterAction, funder reports | Ground in MMF's scale (~20 staff, <$2M) |
| **Policy / regulation** | Government databases, CITES, CMS, RFMOs | Check vault policy notes first |
| **General** | Web search, credible news, institutional reports | Default domain |

## Source tiering (for synthesis)

Weight sources by quality during synthesis:

1. Peer-reviewed literature (highest)
2. Institutional reports (government, IUCN, major NGOs)
3. Established news outlets
4. Blogs, forums, grey literature
5. Vault notes from Simon's own research — high-trust for MMF-specific facts, but treat as prior context that may need freshness checks

## Data collection techniques

**Reddit threads**: Append `/.json` to any Reddit thread URL (e.g. `https://reddit.com/r/sub/comments/xxx/title/.json`) to retrieve full structured JSON including all comments, scores, and metadata. No API key required. Useful for mining community consensus, common objections, practitioner experience, and real-world usage reports. Particularly valuable for technology/tool evaluations and conservation practitioner perspectives.

## Future integrations (deferred)

API integrations for future iterations:
- Semantic Scholar API — academic literature search
- IUCN Red List API v4 — species data
- GBIF / OBIS — occurrence data
- FishBase — species reference data
- OpenAlex — comprehensive academic coverage

Current version uses WebSearch/WebFetch only.
