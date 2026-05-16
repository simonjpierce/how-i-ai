---
name: mmf-brand
description: Apply Marine Megafauna Foundation (MMF) brand identity — colors, typography, logos, spelling, layout — to any MMF-facing artifact. Use when generating MMF slides, posters, infographics, document templates, social media graphics, donor/funder materials, board pack layouts, or any visual artifact that should carry MMF's look-and-feel. Also use when the user says "MMF brand", "MMF style", "use the MMF colors", "apply MMF branding", or "/mmf-brand". Do NOT use for scientific manuscripts (those follow journal style) or personal Planet Ocean / photography content (different brand).
---

# MMF Brand Styling

Apply MMF's visual identity when generating MMF-facing artifacts. **This skill is the current canonical source for MMF brand application** — colours, typography, logo inventory, and selection rules. The 2016 *MMF Brand Manual* (in `02_MARINE MEGAFAUNA/EXTERNAL COMMS/MMF Brand Manual.md`) is a useful background reference for the original design intent but parts are out of date — trust this skill over the manual where they differ.

## When something goes wrong

If a step in this skill fails or needs a workaround, update this skill file with what you learned BEFORE continuing. Add the failure mode, correct any wrong assumption, fix paths or mappings. Examples worth capturing: a logo path that no longer resolves, a font that isn't installed, a tool that won't accept a hex code in a particular format, a colour mapping that turned out to be wrong on visual check.

## Quick reference (most-used)

- **Primary colour:** Dark Cyan `#007987`
- **Secondary:** JK Black `#3f4444`
- **Accent (sparingly):** Coral `#f47C57`
- **Headings:** Futura Std Heavy, uppercase, Dark Cyan
- **Subheadings:** Futura Std Medium Condensed, uppercase, JK Black
- **Body:** Futura Std Book/Heavy 10–12 pt, black (white on dark) — or Source Serif Pro 10–12 pt for text-heavy reports
- **Spelling:** Audience-driven — American English (organization, center, program) for US-audience MMF artifacts; NZ/UK English for international / scientific audiences. See full rule in *Spelling and tone* below.
- **Logo placement:** top-left or bottom-left; minimum 1 cm; do not stretch or recolour
- **Page margins:** ≥1 cm; long body text in 2 columns with 5 mm gap

## Brand colours

### Primary palette

| Role | Name | Hex | RGB | CMYK | Pantone |
|---|---|---|---|---|---|
| Lead | **Dark Cyan** | `#007987` | 0, 121, 135 | C87 M38 Y41 K8 | 7474C |
| Support | **JK Black** | `#3f4444` | 63, 68, 68 | C54 M27 Y36 K82 | 446C |

Use Dark Cyan as the dominant brand colour. JK Black supports it for subheadings, secondary marks, and dark text on light backgrounds.

### Shade scales (graphs, complex graphics only)

For each primary colour, derive shades at 100% / 60% / 30% / 15% opacity. Use only when distinguishing data series in charts, infographics, or posters — not in body content.

### Accent — Coral (use sparingly)

| Name | Hex | RGB | CMYK |
|---|---|---|---|
| **Coral** | `#f47C57` | 244, 124, 87 | C0 M64 Y69 K0 |

Coral highlights stand-out content: a quoted figure, a focus place name on an infographic, a callout number. Restricted to brief sentences, quotes, or numbers in posters and infographics. Do not use for body text or large blocks.

## Typography

Brand fonts (in order of preference):

- **Futura Std** (primary) — Heavy / Medium Condensed / Book — for print, audiovisual, web.
- **Source Serif Pro** (secondary) — Regular / Semibold / Bold — for text-heavy documents (reports, papers, press releases) where Futura body weight feels too dense.

| Element | Font | Size | Colour |
|---|---|---|---|
| Heading | Futura Std Heavy, UPPERCASE | 40 pt | Dark Cyan `#007987` |
| Subheading | Futura Std Medium Condensed, UPPERCASE | 30 pt | JK Black `#3f4444` |
| Body (Futura) | Futura Std Book and Heavy | 10–12 pt | Black (white on dark) |
| Body (Source Serif) | Source Serif Pro Regular / Semibold / Bold | 10–12 pt | Black |

**Font fallbacks** if Futura Std / Source Serif Pro aren't available in the rendering environment: use a clean geometric sans (e.g. Avenir, Century Gothic, Montserrat) for headings and a transitional serif (e.g. Source Serif, Georgia) for body. Note the substitution explicitly in the artifact's notes so Simon can swap in the real fonts when finalising.

## Logos

Logo files live alongside this skill at `~/.claude/skills/mmf-brand/assets/logos/`, in two subfolders. (The vault location `02_MARINE MEGAFAUNA/EXTERNAL COMMS/Logos/` now only holds a README pointing here.)

### MMF Global — `assets/logos/MMF Global/`

| File | Brand Manual variant | Treatment | Typical use |
|---|---|---|---|
| `Marine-Megafauna-Foundation_LOGO.svg` | (A) Extended | Primary on transparent | **Vector master** — use whenever the rendering target accepts SVG (web, modern slide tools, anything that scales). Always prefer this over the PNGs. |
| `Marine-Megafauna-Foundation_LOGO.png` | (A) Extended | Primary on transparent | High-res raster master (~229 KB) — use when SVG isn't accepted. |
| `MMF_logo_new.png` | (A) Extended | Primary on transparent | Legacy 2018 high-res PNG (~3.8 MB). Use only when the master files above are inadequate. |
| `MMF_logo_new_HORIZONTAL.png` | (B) Horizontal | Primary on transparent | Letterhead, newsletters, papers, text documents. |
| `MMF_logo_new_VERTICAL.png` | (C) Vertical | Primary on transparent | Posters where extended doesn't fit; vertical-orientation graphics. |
| `MMF_vertical_logo_initials.png` | (D) Vertical w/ initials | Primary on transparent | Posters/documents where the foundation name has already been spelled out elsewhere. |
| `MMF-icon.png` | (E) Logo solo | Primary on transparent | Favicon, avatar, social profile picture, ID. |
| `MMF_main_logo_white.png` | (A) Extended | **White on transparent** | Use on dark photographic backgrounds or Dark Cyan panels. |
| `MMF_logo_white.png` | (E) Logo solo | **White on transparent** | Icon for use on dark backgrounds. |
| `MMF_vertical_logo_white.png` | (C) Vertical | **White on transparent** | Vertical layout on dark backgrounds. |

### Mozambique — `assets/logos/Mozambique AMM/`

Use the AMM (Associação Megafauna Marinha) logo set for **Mozambique-specific materials only** — Mozambique-language documents, AMM-led local programmes, materials produced for Mozambican government / community audiences. For everything else (international funders, global comms), use the MMF Global set above.

| File | Treatment | Notes |
|---|---|---|
| `AMM_main_logo.png` | Primary on transparent | Equivalent to MMF (A) Extended — default for AMM materials. |
| `AMM_secondary_logo.png` | Primary on transparent | Alternate horizontal lockup. Use when `AMM_main_logo` doesn't fit. *(Not formally specified in the 2016 Brand Manual — verify intended use with Simon before placing in a high-stakes artifact.)* |
| `AMM_vertical_logo.png` | Primary on transparent | Equivalent to MMF (C) Vertical. |
| `AMM_main_logo_white.png` | **White on transparent** | Main lockup for dark backgrounds. |
| `AMM_secondary_logo_white.png` | **White on transparent** | Secondary lockup for dark backgrounds. |
| `AMM_vertical_logo_white.png` | **White on transparent** | Vertical lockup for dark backgrounds. |
| `AMM_tagline.png` | Primary on transparent | Tagline lockup variant. *(Not in the 2016 Brand Manual — purpose unclear without context. Verify before placing in a high-stakes artifact.)* |

### Mapping verification

The variant assignments above are inferred from filenames and the 2016 Brand Manual's variant scheme — they have not been visually confirmed against the manual's variant illustrations. Before finalising any high-stakes artifact, open the chosen file and confirm it matches the intended variant. If a mismatch is found, correct the tables above.

### Still missing

- **AMM Variant D (vertical with initials)** and **AMM Variant E (logo solo / icon)** — not located in the search of Drive on 2026-04-26. If a Mozambique artifact needs these, ask Simon to source from the design team rather than improvising.
- **EPS / AI vector formats** — only the MMF Global SVG was found. If a print designer requests EPS/AI, ask Simon to source.

### Selection rules

1. **Vector first.** When the rendering target accepts SVG, use `Marine-Megafauna-Foundation_LOGO.svg`. Always.
2. **Match the entity to the audience.** MMF Global for international/donor/scientific/global; Mozambique AMM for Mozambique-specific work in country.
3. **Match the treatment to the background.** Primary (Dark Cyan) on light backgrounds; **white** on dark photographic backgrounds, dark coloured panels, or anywhere a primary-colour logo would lose contrast.
4. **Pick the lockup that fits the space.** Extended (A) is the default. Horizontal (B) for narrow horizontal strips (letterheads). Vertical (C) for tall narrow spaces. Variant (D) only when the foundation name appears elsewhere on the same artifact. Icon (E) for favicons, avatars, square ID slots.
5. **Never recolour.** The Brand Manual prohibits colour changes. If neither the primary nor the white treatment works, change the background — don't change the logo.

### Logo usage rules (verbatim from the Brand Manual)

- **Clear space:** keep an area free of other elements around the logo, sized to the turtle in the wordmark.
- **Placement:** prefer top-left; bottom-left is acceptable.
- **Minimum size:** the logo must be no smaller than **1 cm** on the rendered page; on screen, scale so the wordmark stays legible.
- **Proportions:** never stretch, squash, or skew. Resize proportionally only.
- **Colour:** never recolour the logo. Acceptable backgrounds are (A) primary colour on white, or (B) white on a primary-colour panel.
- **On photos:** choose a variant that contrasts with the image; do not place over busy areas where the wordmark loses legibility.

### Co-branded layouts

- MMF-led project: MMF logo top-left; partner logos top-right.
- Externally funded project: MMF logo top; sponsor logos along the bottom (smaller if many).

## Spelling and tone

- **Spelling:** Audience-driven, not blanket. **American English** for US-audience MMF artifacts — board decks, US-donor materials, US-grant applications, anything with the MMF Inc. entity as the primary voice (*organization* not *organisation*, *center* not *centre*, *program* not *programme*). **NZ/UK English** for international / scientific audiences — conference talks, scientific presentations, international funder decks (these match the vault default). When the audience is ambiguous, confirm with Simon before drafting. *Updated 2026-04-27 — earlier blanket "American English throughout MMF content" rule narrowed to US-audience output specifically; conference / scientific contexts join scientific manuscripts in following journal/audience convention.*
- **Tone:** professional, evidence-based, accessible to non-specialist audiences (donors, board, partners). See `02_MARINE MEGAFAUNA/CLAUDE.md` for the full MMF tone guidance, and `05_SYSTEM/Voice References/` for format-specific voice guides.
- **Brand expression:** *"Saving ocean giants from extinction."*
- **Brand purpose touchstone:** *"United for the future of marine life."*

## Layout defaults

Apply these unless the artifact's brief specifies otherwise:

- **Page margins:** at least 1 cm of clear space between content and page edge.
- **Logo placement:** top-left when possible (bottom-left as fallback).
- **Body text columns:** for long-form copy, split into two columns with a 5 mm gutter.
- **Imagery:** prefer large megafauna photographs; a half-page image can occupy a full column.
- **Charts and graphs:** use the primary palette and its shade scales to distinguish data series; reserve Coral for a single emphasised value.

## When NOT to apply this skill

- **Scientific manuscripts and journal submissions** — follow the target journal's style guide, not MMF brand. Manuscripts carry MMF affiliation, not MMF visual identity.
- **Planet Ocean / `simonjpierce.com` / `naturetripper.com` / Sony partnership content** — separate personal/photography brand. See `03_PLANET OCEAN/CLAUDE.md`.
- **Personal correspondence or non-work output** — no MMF styling needed.
- **Internal-only working documents** (lab notebooks, private project notes) — plain markdown is fine; MMF brand is for external-facing artifacts.

## Cross-references

- Logo files: `~/.claude/skills/mmf-brand/assets/logos/` (canonical)
- Background brand manual (2016, partially dated): `02_MARINE MEGAFAUNA/EXTERNAL COMMS/MMF Brand Manual.md`
- MMF folder context (tone, team, funders): `02_MARINE MEGAFAUNA/CLAUDE.md`
- Voice guides for specific formats: `05_SYSTEM/Voice References/`
