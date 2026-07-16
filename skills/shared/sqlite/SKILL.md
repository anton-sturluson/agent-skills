---
name: sqlite
description: "Query the local investor SQLite database (invest.db) via the sqlite3 CLI. Use when reading or writing companies, theses, decisions, notes, or watchlist data, or any time you need to look up investment-process records."
---

# SQLite — Investor DB

Local system of record for the investment process. No server, no wrapper — drive it with the `sqlite3` CLI that ships with macOS.

## Database

```
DB=/Users/charlie-buffet/Documents/project-minerva/hard-disk/data/04-database/invest.db
```

Tables: `companies`, `theses`, `decisions`, `notes`, `watchlist`. Inspect anything with:

```
sqlite3 "$DB" ".tables"
sqlite3 "$DB" ".schema companies"
```

### companies (the main table)

| Column | Type | Notes |
|---|---|---|
| id | INTEGER PK | rowid |
| ticker | TEXT UNIQUE | nullable (private/pre-IPO ok) |
| name | TEXT | company name |
| sector | TEXT | optional |
| description | TEXT | business overview |
| categories | TEXT | JSON array of tags, e.g. `["SaaS","Vertical SaaS"]` |
| folder_exists | INTEGER | 1 if a folder exists in `reports/00-companies/`, else 0 |
| created_at / updated_at | TEXT | timestamps |

## Reading

Use `-json` for parseable output (preferred for agents):

```
sqlite3 "$DB" -json "SELECT ticker, name FROM companies WHERE folder_exists=1"
```

`categories` is JSON text — query tags with `json_each`:

```
# all companies tagged SaaS
sqlite3 "$DB" -json "SELECT ticker, name FROM companies WHERE categories LIKE '%\"SaaS\"%'"

# category counts
sqlite3 "$DB" "SELECT je.value AS category, COUNT(*) AS n
               FROM companies, json_each(companies.categories) je
               GROUP BY category ORDER BY n DESC"
```

## Writing

Always enable foreign keys (per-connection, not persisted):

```
sqlite3 "$DB" "PRAGMA foreign_keys=ON;
  INSERT INTO companies (ticker, name, description, categories, folder_exists)
  VALUES ('MSFT','Microsoft','...', '[\"SaaS\"]', 1);"
```

Update a tag list or folder flag:

```
sqlite3 "$DB" "UPDATE companies SET folder_exists=1, updated_at=datetime('now') WHERE ticker='DDOG';"
```

To append a category, read the JSON, add the tag, write it back (SQLite has no array append in plain SQL — do it in a small script if touching many rows).

## Notes

- WAL mode is on; `invest.db-wal` / `invest.db-shm` sidecars are normal — never edit/delete them while the DB is in use.
- Scope is the qualitative investment layer. Mechanical holdings/transactions live in `hard-disk/data/01-portfolio/` as JSON — do not duplicate them here.
- When adding/removing a company folder under `reports/00-companies/`, keep `companies.folder_exists` truthful (see shared AGENTS.md "Investor DB").
- Schema source: `hard-disk/data/04-database/schema.sql` (idempotent; re-runnable).
