---
name: x-search-query
version: 1.0.0
description: Build paste-ready X (Twitter) advanced search queries for ANY topic — operator combinations for viral gold, fresh trends, article gold, demos, and account research. Run whenever the user wants to hunt posts on X for research, inspiration, or competitor intel.
updated: 2026-09-05
status: active
---

# X Advanced Search Query Builder

Turns any topic into a set of ready-to-paste X advanced search queries. The user copies them into the X search bar and gets clean, high-signal results. No API, no scraping: this is a search-bar playbook.

## When used

User gives a topic (any niche) and wants X search queries to paste. Optionally gives an intent, a timeframe, or named accounts.

## Inputs

- **Topic** (required) — can be a phrase, a product, a concept, a person's field
- Optional: intent (viral inspiration / fresh trends / deep-dive articles / demos / a specific account's best posts)
- Optional: timeframe (24h, week, ever)
- Optional: named accounts for account-level research

## Method

### 1. Decompose the topic into searchable terms

Split the topic into 4-8 surface variants an author would actually type:
- Exact phrases in quotes: `"model context protocol"`, `"local first"`
- Aliases and abbreviations: `MCP` for "Model Context Protocol", `RAG` for "retrieval augmented generation"
- Community jargon and misspellings the niche actually uses
- One or two adjacent concepts (only when they sharpen results, not broaden them)

Do NOT overstuff. One giant OR chain dilutes precision. Prefer 2-3 term sets used across separate queries.

### 2. Pick negative terms (noise exclusion)

Derive exclusions from the topic. Baseline X spam that pollutes tech/AI/creator niches: `-giveaway -airdrop -presale -signup` plus category spam (`-crypto -nft -memecoin`) ONLY when the topic is not itself crypto/web3. If the topic IS the spam category, drop the matching exclusions. When unsure, exclude less: one wrong `-` term silently removes good results.

### 3. Pick the operator preset (below)

Query intents and what each surfaces:

| Preset | Core operators | Use when |
|---|---|---|
| Pulse | topic terms, no filters | See what the space is saying right now |
| Viral gold | topic terms + min_faves/min_retweets + -filter:replies | Proven posts worth studying or citing |
| Fresh trends | topic terms + within_time:24h (or 7d) + modest min_faves | Something hot happening now |
| Article gold | topic terms + filter:links + min_faves | News, essays, and link-worthy reads |
| Demo gold | topic terms + filter:media + min_faves | Screenshots, videos, live demos |
| Account research | from:<handle> combos | One account's best-performing posts |

Engagement floors are niche-dependent, state your assumption:
- Big mainstream tech (AI, coding): `min_faves:250` + `min_retweets:50`
- Mid-size niches (data engineering, DevOps): `min_faves:100` + `min_retweets:25`
- Small/emerging niches: `min_faves:25` or drop the floor entirely

When in doubt, give the user a high-floor and a low-floor variant of the same query.

### 4. Assemble queries

Standard shapes (fill terms, floors, negatives):

```
(topic OR "phrase" OR alias) min_faves:250 -filter:replies lang:en -noise1 -noise2
("exact phrase" OR alias) min_retweets:25 -filter:replies lang:en
(topic OR "phrase") filter:links min_faves:100 lang:en
(topic OR alias) filter:media min_faves:100 lang:en
(topic OR alias) within_time:24h min_faves:25 lang:en
from:handle (topic OR "phrase") min_faves:50
```

## Output format

For each intent, label what it surfaces, then one code line to copy. Put all paste lines in a single code block at the end so the user can grab them one at a time.

```markdown
# X search queries — <topic>   (<assumed niche size>: floor assumption stated)

## Viral gold (proven posts worth studying)
paste-able query line

## Fresh trends (last 24h)
paste-able query line

## Article gold (link posts)
paste-able query line

## Demo gold (media posts)
paste-able query line

## Account research
from:handle paste-able query line   (only when accounts are relevant)

## Paste box
one code block, one query per line, plain
```

## Gotchas (tell the user when relevant)

- **Empty results**: an over-aggressive OR chain or `min_faves` floor is usually the cause. Remedy: split the OR groups into separate queries, then drop `min_faves` and re-add in steps.
- **Exact phrases in quotes win**: quoted phrases outrank loose keywords. Every query set needs at least one quoted variant.
- **`-filter:replies` keeps root posts**: use it when the goal is original posts; drop it when hunting discussions to join.
- **`within_time:Nh` is relative to now**: use it for fresh-trend hunting; use the X UI date pickers instead when the user needs a fixed past window.
- **Search is account-specific on X**: what an account with few followers sees differs from a large one. If results look thin, the floor is too high for that viewer.

## Example (worked, for a mid-size niche)

Topic: "MCP servers". Terms: `"MCP server"`, `"Model Context Protocol"`, `MCP`, `"tool servers"`. Floors: min_faves:100 / min_retweets:25. Negatives: -giveaway -airdrop -crypto.

Viral gold:
`("MCP server" OR "Model Context Protocol") min_faves:100 -filter:replies -giveaway -airdrop`

Fresh:
`(MCP OR "MCP server") within_time:24h min_faves:25 lang:en`

Article gold:
`("MCP server" OR MCP) filter:links min_faves:100 lang:en`

Rule: the model does the decomposition and floor math per topic. Never return generic templates without filling in real topic terms.
