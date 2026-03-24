import json
import os
import time
from scholarly import scholarly, ProxyGenerator

# ── Config ──────────────────────────────────────────────────
SCHOLAR_ID = os.environ["SCHOLAR_ID"]   # set as GitHub Actions secret
OUTPUT_FILE = "publications.json"
DELAY_BETWEEN_FILLS = 2   # seconds — be polite to Google
# ────────────────────────────────────────────────────────────

print(f"Fetching author profile for Scholar ID: {SCHOLAR_ID}")

# Optional: use a free proxy to reduce chance of being rate-limited
# pg = ProxyGenerator()
# pg.FreeProxies()
# scholarly.use_proxy(pg)

# Step 1: get the author record
author = scholarly.search_author_id(SCHOLAR_ID)

# Step 2: fill author profile — this fetches ALL publications
# sortby='pubdate' ensures newest-first; set to 'citations' for most-cited-first
author = scholarly.fill(author, sections=["basics", "publications"], sortby="pubdate")

total_raw    = len(author.get("publications", []))
total_cites  = author.get("citedby", 0)
h_index      = author.get("hindex", 0)
i10_index    = author.get("i10index", 0)

print(f"Found {total_raw} publication entries on Scholar profile")
print(f"Total citations (from profile): {total_cites} | h-index: {h_index} | i10: {i10_index}")

# Step 3: fill EACH publication individually to get exact cited-by count
pubs = []
for i, pub in enumerate(author["publications"]):
    try:
        filled = scholarly.fill(pub)   # fetches exact citation count per paper
        time.sleep(DELAY_BETWEEN_FILLS)
    except Exception as e:
        print(f"  Warning: could not fill pub {i+1} — using partial data ({e})")
        filled = pub

    bib = filled.get("bib", {})

    title   = bib.get("title", "").strip()
    if not title:
        continue    # skip empty entries

    pubs.append({
        "title":    title,
        "authors":  bib.get("author", ""),
        "journal":  bib.get("journal") or bib.get("booktitle") or bib.get("publisher") or "",
        "year":     bib.get("pub_year", ""),
        "url":      filled.get("pub_url", "") or bib.get("url", ""),
        "cited_by": filled.get("num_citations", 0),
        "abstract": bib.get("abstract", ""),
    })
    print(f"  [{i+1}/{total_raw}] {title[:70]}… — cited by {pubs[-1]['cited_by']}")

# Sort newest first
pubs.sort(key=lambda x: str(x.get("year") or "0"), reverse=True)

# Save summary alongside the publications
output = {
    "meta": {
        "scholar_id":   SCHOLAR_ID,
        "total_pubs":   len(pubs),
        "total_cites":  total_cites,
        "h_index":      h_index,
        "i10_index":    i10_index,
        "last_updated": __import__("datetime").datetime.utcnow().isoformat() + "Z"
    },
    "publications": pubs
}

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"\nDone! Saved {len(pubs)} publications to {OUTPUT_FILE}")
print(f"Total citations: {total_cites} | h-index: {h_index} | i10-index: {i10_index}")
