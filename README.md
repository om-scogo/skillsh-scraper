# skillsh-scraper

A tiny Python scraper for **skills.sh** that uses the **official API**:

- Base: `https://skills.sh/api/v1/`
- Endpoint used: `GET /skills`
- Auth: `Authorization: Bearer <Vercel OIDC token>`

It writes output in the same JSON shape as:
`/home/ubuntu/skills-api/src/registry/scraped-skills.json`

## Files

- `main.py` — main script

## Requirements

- Python 3.11+
- A valid `skills.sh` Vercel OIDC token (no key generation needed)

## Run

```bash
cd /home/ubuntu/skillsh-scraper
python3 main.py --token "<your-token>"
```

Defaults:

- output path: `./scraped-data/scraped-skills.json` (relative to this folder)
- view: `all-time`
- per_page: `500`

## Optional args

```bash
python3 main.py \
  --token "<token>" \
  --view all-time \
  --per-page 500 \
  --output ./scraped-data/scraped-skills.json
```

## Env vars

Instead of `--token`, you can set:

- `VERCEL_OIDC_TOKEN`
