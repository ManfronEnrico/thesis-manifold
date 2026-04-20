---
title: Nielsen Data Access & Local Backup Strategy
type: note
status: active
created: 2026-04-20
---

# Nielsen Data Access & Local Backup Strategy

## Context

Nielsen data is accessed via Microsoft Fabric Data Warehouse using an Azure AD app registration.
Authentication uses a client secret (expires periodically). When the secret expires, access is lost
until regenerated — and any unsnapshotted data becomes temporarily inaccessible.

## Authentication Flow

1. App registration in Azure AD identified by **App (Client) ID**: `f0460586-525d-4d1e-adb7-c5b6dfd26aab`
2. Client secret regenerated via Azure Portal (Owner/Contributor role on the app registration required)
3. New secret value stored in `.env` as `RU_CLIENT_SECRET` (shown only once at generation — copy immediately)
4. Python connection script reads from `.env` and re-establishes the Fabric DW connection

## Local Backup Strategy

After a successful connection, a snapshot of the dataset is written to a local encrypted file.

**Encryption approach**: AES-256 via the `cryptography` Python library (Fernet wrapper).

- A symmetric encryption key is generated once and stored in `.env` as `NIELSEN_ENCRYPTION_KEY`
- The snapshot is saved as an encrypted binary file (e.g. `nielsen_snapshot.csv.enc`)
- Both `.env` and `*.enc` files are covered by `.gitignore` — never committed to the repo
- The encryption key is shared with collaborators out-of-band (e.g. Signal), never via the repo

**Why AES-256 / Fernet:**
- AES-256-CBC with HMAC-SHA256 — standard for symmetric encryption of sensitive research data
- Fernet is authenticated encryption: detects tampering in addition to providing confidentiality
- Sufficient for local storage of survey/consumer data under GDPR research exemptions

## Reproducibility

Both Brian and Enrico maintain their own local encrypted snapshots. The connection + snapshot
script is committed to the repo (without secrets), so either collaborator can:

1. Add their `.env` with the shared key and regenerated secret
2. Run the script to pull fresh data or decrypt the existing snapshot
3. Proceed with analysis notebooks without waiting for a full Fabric reconnection

## Files

| File | Tracked? | Purpose |
|------|----------|---------|
| `scripts/nielsen_connection.py` | ✅ YES | Connection + snapshot logic (no secrets) |
| `.env` | ❌ NO | `RU_CLIENT_SECRET`, `NIELSEN_ENCRYPTION_KEY` |
| `datasets/nielsen_snapshot.csv.enc` | ❌ NO | Encrypted local data snapshot |

## Action Items

- [ ] Regenerate client secret (via Nika or Azure Portal)
- [ ] Update `RU_CLIENT_SECRET` in `.env`
- [ ] Re-run connection script and write encrypted snapshot
- [ ] Share `NIELSEN_ENCRYPTION_KEY` with Enrico out-of-band
