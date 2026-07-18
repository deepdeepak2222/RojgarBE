# Coding Rules

These rules apply to the entire RojgarApp codebase (backend + frontend).
Keep them short, keep them enforced.

## 1. Functions stay small

- **No function may exceed 30 lines** (excluding blank lines and the signature).
- A function does **one** thing. If you need "and" to describe it, split it.
- Max 4 parameters per function. More than that → pass an object/dataclass.

## 2. One feature, one package

- Every feature lives in **its own package**.
  - Backend: a dedicated Django app (e.g. `parties/`, `items/`, `invoices/`).
  - Frontend: a dedicated feature folder (e.g. `features/parties/`).
- A feature never imports the internals of another feature. Share code only
  through a clearly-named `core`/`common` package.

## 3. Files stay small

- A source file should stay under ~200 lines. Split when it grows past that.
- One primary responsibility per file (one model group, one screen, etc.).

## 4. Naming

- Names are descriptive and full words: `customer_phone`, not `cph`.
- Booleans read as questions: `is_active`, `has_balance`.
- No abbreviations except well-known ones (`id`, `url`, `api`).

## 5. Constants live in a constants file

- **No magic strings/numbers** scattered in logic.
- Every package keeps its constants in a dedicated **`constants.py`** (backend)
  or **`constants.ts`** (frontend) in that same folder — import from there.
- Genuinely global config goes in Django settings / env, not a constants file.
- Secrets and environment-specific values come from **environment variables only**
  and are never committed.

## 6. Comments

- Comment **why**, never **what**. The code already says what it does.
- No commented-out code in commits.

## 7. Errors

- Never silently swallow errors. Handle, log, or re-raise.
- Validate input at the boundary (serializers on the backend, forms on the UI).

## 8. Types

- Backend: use type hints on function signatures (params and return).
- Frontend: no `any`. Prefer explicit types/interfaces; let `tsc` stay green.

## 9. Layers (backend)

Keep a clear flow: `model → serializer → view → url`.
Business logic that is more than trivial goes into a `services.py`, not the view.

## 10. Multi-tenancy (row-level)

- One shared database. **Every business entity belongs to a `Client`.** Inherit
  `core.models.TenantOwnedModel` so the `client` FK (with cascade delete) is
  added consistently — don't redeclare it per model.
- **Never trust a client id from the request.** The active client comes from the
  logged-in user (`core.scoping.get_current_client`).
- Tenant-scoped APIs must use `core.scoping.ClientScopedViewSet` (or filter by
  the current client) and require authentication. Never return unscoped data.
- Deleting a `Client` must cascade to all of its data.

## 11. Tests

- Every feature package ships with at least basic tests.
- **Tests must pass before every push** — this is enforced by a git pre-push
  hook (see below), but don't rely on it: run them yourself.

## 12. Commits & quality gates

- Run linters/formatters before committing (`ruff`/`black` for Python,
  `eslint`/`prettier` for TypeScript).
- Small, focused commits with a clear message (what + why).
- Never commit secrets, `.env`, `node_modules`, build output, or IDE folders.

---

## Enforcement (pre-push hook)

Each repo ships a `.githooks/pre-push` that runs the checks before a push:

- **Backend** (`RojgarBE`): runs `python manage.py test` (via Docker).
- **Frontend** (`RojgarFE`): runs `tsc --noEmit`.

Enable it once per clone (hooks path isn't shared automatically by git):

```bash
git config core.hooksPath .githooks
```

A failing check aborts the push. To bypass in an emergency: `git push --no-verify`.
