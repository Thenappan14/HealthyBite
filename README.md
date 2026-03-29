# PlateWise

PlateWise is a full-stack monorepo for personalized restaurant menu recommendations. Users build a food profile, upload menu screenshots or PDFs, or paste a restaurant URL. The system extracts dishes, estimates likely nutrition, filters unsafe options, and ranks menu items with transparent explanations.

Recommendations are based on estimated nutrition and provided profile information. This is not medical advice.

## Monorepo structure

```text
.
|-- backend/
|   |-- app/
|   |   |-- api/
|   |   |-- core/
|   |   |-- db/
|   |   |-- models/
|   |   |-- schemas/
|   |   |-- services/
|   |   |-- init_db.py
|   |   |-- main.py
|   |   `-- seed.py
|   |-- sample_data/
|   |-- storage/uploads/
|   |-- .env.example
|   `-- requirements.txt
|-- docs/
|   |-- api.md
|   |-- architecture.md
|   `-- database-schema.sql
|-- frontend/
|   |-- app/
|   |-- components/
|   |-- lib/
|   |-- .env.example
|   |-- package.json
|   `-- tailwind.config.ts
`-- .env.example
```

## Stack

- Frontend: Next.js, TypeScript, Tailwind CSS, shadcn-style UI primitives
- Backend: FastAPI, SQLAlchemy, Pydantic, PostgreSQL
- Ingestion: OCR placeholder pipeline for uploads, heuristic website parser for restaurant URLs
- Scoring: hard filters plus hybrid soft scoring for profile fit

## Backend setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python -m app.init_db
python -m app.seed
uvicorn app.main:app --reload
```

API runs at `http://localhost:8000`, Swagger at `http://localhost:8000/docs`.

### Demo authentication

For a lightweight scaffold, authenticated endpoints accept an `X-User-Id` header. The seed script creates:

- Email: `demo@platewise.app`
- Password: `demo1234`
- Demo user id: `1`

## Frontend setup

```bash
cd frontend
npm install
copy .env.example .env.local
npm run dev
```

Frontend runs at `http://localhost:3000`.

## Key product flows

1. Sign up or log in.
2. Complete the profile at `/profile`.
3. Upload a menu at `/upload` or paste a restaurant URL at `/analyze-url`.
4. Review ranked dishes at `/results`.
5. Inspect recommendation history at `/saved`.

## API summary

- `POST /api/auth/signup`
- `POST /api/auth/login`
- `GET /api/profile`
- `PUT /api/profile`
- `POST /api/uploads`
- `POST /api/ingest/url`
- `POST /api/recommendations/{menu_id}`
- `GET /api/history`

Detailed request and response notes are in [docs/api.md](/c:/Users/Projects/HealthyBite/docs/api.md).

## Notes on estimation and safety

- Nutrition values are estimated from menu wording and likely ingredients.
- Allergens are inferred heuristically and should be treated as warnings, not guarantees.
- The system avoids medical claims and uses cautious wording throughout the API and UI.
- The OCR and crawler layers are intentionally scaffolded so you can swap in production OCR, vision, or LLM extraction later.

## Seed and sample data

- Upload sample: [backend/sample_data/sample_menu_upload.txt](/c:/Users/Projects/HealthyBite/backend/sample_data/sample_menu_upload.txt)
- Website parser sample payload: [backend/sample_data/sample_restaurant_payload.json](/c:/Users/Projects/HealthyBite/backend/sample_data/sample_restaurant_payload.json)

## Suggested next improvements

- Replace demo header auth with JWT bearer auth on protected routes.
- Add Alembic migrations and background jobs for OCR/crawling.
- Swap placeholder nutrition inference for a stronger ingredient knowledge base or model-assisted extraction.
- Add file persistence, S3 support, and OCR providers for production use.

