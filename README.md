# Digital Governance Paper Notes

Short, practitioner-oriented reviews of research and policy papers on:

- AI governance and institutional impacts
- Digital public infrastructure (DPI) and public sector delivery
- Digital identity, trust infrastructure, and interoperability
- Internet governance, privacy, and security

Most notes are ~1500–2000 characters and are often drafted for LinkedIn first, then archived here.

---

## Repository Structure

- `reviews/YYYY/` – canonical review notes (stable naming convention)
- `index.md` – auto-generated index of all reviews (do not hand-edit)
- `templates/` – writing templates
- `taxonomy/` – controlled vocabulary (domains, tags)
- `scripts/` – repo utilities (index builder)
- `legacy/` – older paths kept for backward compatibility

---

## Review File Convention

New reviews should be created under:

`reviews/YYYY/YYYY-MM-DD__<slug>__v1.md`

Each review **should** start with front matter:

```yaml
---
title: ""
source: ""
publication: ""
date_read: "YYYY-MM-DD"
primary_domain: ""
tags: []
---
```

Use: `templates/review-template.md`

---

## Index Generation

The index is generated from front matter in review files.

Rebuild locally:

```bash
python scripts/build_index.py
```

CI checks that `index.md` is up to date on every push/PR.

---

## License

See `LICENSE`.
