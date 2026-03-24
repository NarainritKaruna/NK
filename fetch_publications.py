import json
import os
from scholarly import scholarly

# Your Google Scholar ID is passed in via GitHub Actions secret
scholar_id = os.environ["SCHOLAR_ID"]

print(f"Fetching publications for Scholar ID: {scholar_id}")

author = scholarly.search_author_id(scholar_id)
author = scholarly.fill(author, sections=["publications"])

pubs = []
for pub in author["publications"]:
    p = pub.get("bib", {})
    pubs.append({
        "title":    p.get("title", ""),
        "authors":  p.get("author", ""),
        "journal":  p.get("journal") or p.get("booktitle", ""),
        "year":     p.get("pub_year", ""),
        "url":      pub.get("pub_url", ""),
        "cited_by": pub.get("num_citations", 0)
    })

# Sort by year descending (newest first)
pubs.sort(key=lambda x: x["year"] or "0", reverse=True)

with open("publications.json", "w", encoding="utf-8") as f:
    json.dump(pubs, f, indent=2, ensure_ascii=False)

print(f"Done! Saved {len(pubs)} publications to publications.json")
