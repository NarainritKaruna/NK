import json
import os
import time
from scholarly import scholarly

scholar_id = os.environ["SCHOLAR_ID"]

print(f"Fetching publications for Scholar ID: {scholar_id}")

# Get author with publications
author = scholarly.search_author_id(scholar_id)
author = scholarly.fill(author, sections=["publications"])

pubs = []
total_citations = 0

for pub in author["publications"]:
    try:
        # 🔥 IMPORTANT: fully fetch each publication
        pub_filled = scholarly.fill(pub)

        bib = pub_filled.get("bib", {})

        citations = pub_filled.get("num_citations", 0) or 0
        total_citations += citations

        # Ensure year is numeric
        year = bib.get("pub_year")
        year = int(year) if year and str(year).isdigit() else 0

        pubs.append({
            "title": bib.get("title", ""),
            "authors": bib.get("author", ""),
            "journal": bib.get("journal") or bib.get("booktitle", ""),
            "year": year,
            "url": pub_filled.get("pub_url", ""),
            "cited_by": citations
        })

        # ⚠️ avoid being blocked by Google Scholar
        time.sleep(1)

    except Exception as e:
        print(f"Skipping a publication due to error: {e}")
        continue

# Sort correctly by numeric year
pubs.sort(key=lambda x: x["year"], reverse=True)

# Save publications
with open("publications.json", "w", encoding="utf-8") as f:
    json.dump(pubs, f, indent=2, ensure_ascii=False)

# Save author metrics separately (more accurate)
metrics = {
    "total_citations_profile": author.get("citedby", 0),
    "h_index": author.get("hindex", 0),
    "i10_index": author.get("i10index", 0),
    "total_citations_calculated": total_citations,
    "num_publications": len(pubs)
}

with open("metrics.json", "w", encoding="utf-8") as f:
    json.dump(metrics, f, indent=2)

print("Done!")
print(f"Publications: {len(pubs)}")
print(f"Total citations (calculated): {total_citations}")
print(f"Total citations (profile): {metrics['total_citations_profile']}")
