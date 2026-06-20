# RojgarApp

A Vyapar-style **multi-tenant SaaS** business app, built feature by feature.
The first feature is **Parties** (managing your customers and suppliers).

## Architecture

| Layer    | Tech                                              | Why                                              |
| -------- | ------------------------------------------------- | ------------------------------------------------ |
| Backend  | Django + DRF + PostgreSQL                          | Batteries-included REST APIs                     |
| Frontend | Expo (React Native + TypeScript) + react-native-web | One codebase for Android, iPhone, and the browser |
| Auth     | JWT (SimpleJWT), email + password                 | Stateless auth for web + mobile                  |
| Infra    | Docker Compose                                     | Reproducible Postgres + backend, no local setup   |

### Multi-tenancy: row-level (shared database)

There is **one URL** and **one shared database**. Every business entity has a
`client` foreign key, and queries are scoped to the logged-in user's client.

- **Self-serve onboarding** — anyone signs up, which creates their `Client`
  (business) plus an owner user, and logs them straight in (JWT).
- **Ownership** — business models inherit `core.models.TenantOwnedModel`, which
  adds `client = ForeignKey(Client, on_delete=CASCADE)`. Deleting a client
  cascades and removes all of its data.
- **Isolation** — `core.scoping.ClientScopedViewSet` filters every read to the
  current client (derived from the user, never from the request) and stamps the
  client on every create. The client id is never trusted from the caller.

Every feature is its own package:

- Backend: a Django app (e.g. `backend/parties/`). Shared building blocks live
  in `core/`; the tenant registry in `clients/`; users/auth in `accounts/`.
- Frontend: a feature folder (e.g. `frontend/src/features/parties/`).

See [`CODING_RULES.md`](./CODING_RULES.md) for the rules we follow.

## Project layout

```
RojgarApp/
├── backend/                 # Django + DRF API
│   ├── config/              # settings, root urls
│   ├── core/                # TenantOwnedModel + client-scoping viewset
│   ├── clients/             # Client (a business / tenant)
│   ├── accounts/            # users<->client membership, JWT signup/login
│   └── parties/             # FEATURE: customers & suppliers
├── frontend/                # Expo app (Android / iOS / web)
│   └── src/
│       ├── core/            # API client, session/token storage
│       └── features/
│           ├── auth/        # signup / login
│           └── parties/     # FEATURE: parties UI
├── docker-compose.yml       # postgres + backend
└── CODING_RULES.md
```

## Run the backend (Docker)

```bash
docker compose up --build
```

This starts PostgreSQL and the Django API at <http://localhost:8000>, applying
migrations on startup. Everything is a single URL; tenancy is row-level.

```bash
# Sign up a new business (creates the client + owner, returns JWT tokens)
curl -X POST http://localhost:8000/api/auth/signup/ \
  -H "Content-Type: application/json" \
  -d '{"business_name":"Acme","email":"o@acme.com","password":"supersecret1"}'

# Log in (JWT)
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"o@acme.com","password":"supersecret1"}'

# Use the API with the access token (scoped to your client automatically)
curl http://localhost:8000/api/parties/ -H "Authorization: Bearer <access>"
```

Admin: create a superuser, then visit <http://localhost:8000/admin/>:

```bash
docker compose exec backend python manage.py createsuperuser
```

Run the tests:

```bash
docker compose exec backend python manage.py test
```

## Run the frontend (Expo)

```bash
cd frontend
cp .env.example .env   # optional: set EXPO_PUBLIC_API_URL
npm run web            # open in the browser
# or
npm run ios            # iOS simulator
npm run android        # Android emulator
```

For a physical phone, install **Expo Go**, run `npm start`, scan the QR code,
and set `EXPO_PUBLIC_API_URL` to your computer's LAN IP.

## What works today

- **Self-serve signup + login** (JWT) — creating a business and using the app
  end to end, in the browser or on a device.
- **Row-level multi-tenancy**: every entity has a `client` FK; reads are scoped
  to the logged-in user's client (verified — businesses can't see each other's
  data); deleting a client cascades all its data.
- **Parties**: create/list customers & suppliers, filter by type
  (`GET /api/parties/?type=customer`); full CRUD on the API, auth required.

## Known gaps / next up

- One user belongs to one business (the owner). **Inviting staff / multiple
  users per client** isn't built yet (the `Membership` model is ready for it).
- No refresh-token rotation/auto-refresh on the frontend yet (12h access token).
- Next features: Items/products → Invoices → Payments → Reports, each as its own
  package on both backend and frontend.
