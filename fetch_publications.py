import json
import os
import time
from datetime import datetime
from scholarly import scholarly

# ── Config ──────────────────────────────────────────────────
SCHOLAR_ID  = os.environ["SCHOLAR_ID"]   # set as GitHub Actions secret
OUTPUT_FILE = "publications.json"
DELAY       = 2   # seconds between fills — be polite to Google
# ────────────────────────────────────────────────────────────

print(f"Fetching author profile for Scholar ID: {SCHOLAR_ID}")

# Step 1: get author record + ALL publications
author = scholarly.search_author_id(SCHOLAR_ID)
author = scholarly.fill(author, sections=["basics", "publications"], sortby="pubdate")

total_cites = author.get("citedby",   0)
h_index     = author.get("hindex",    0)
i10_index   = author.get("i10index",  0)
raw_count   = len(author.get("publications", []))

print(f"Found {raw_count} publications | Citations: {total_cites} | h-index: {h_index} | i10: {i10_index}")

# Step 2: fill each publication individually for exact cited_by count
pubs = []
for i, pub in enumerate(author["publications"]):
    try:
        filled = scholarly.fill(pub)
        time.sleep(DELAY)
    except Exception as e:
        print(f"  Warning: could not fill pub {i+1}: {e}")
        filled = pub

    bib   = filled.get("bib", {})
    title = bib.get("title", "").strip()
    if not title:
        continue

    pubs.append({
        "title":    title,
        "authors":  bib.get("author", ""),
        "journal":  bib.get("journal") or bib.get("booktitle") or bib.get("publisher") or "",
        "year":     bib.get("pub_year", ""),
        "url":      filled.get("pub_url", "") or bib.get("url", ""),
        "cited_by": filled.get("num_citations", 0),
    })
    print(f"  [{i+1}/{raw_count}] {title[:70]}... cited_by={pubs[-1]['cited_by']}")

# Sort newest first
pubs.sort(key=lambda x: str(x.get("year") or "0"), reverse=True)

# Step 3: write output with meta + publications
output = {
    "meta": {
        "scholar_id":   SCHOLAR_ID,
        "total_pubs":   len(pubs),
        "total_cites":  total_cites,
        "h_index":      h_index,
        "i10_index":    i10_index,
        "last_updated": datetime.utcnow().isoformat() + "Z"
    },
    "publications": pubs
}

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"\nDone! Saved {len(pubs)} publications to {OUTPUT_FILE}")
print(f"Citations: {total_cites} | h-index: {h_index} | i10-index: {i10_index}")
