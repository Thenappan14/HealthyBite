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
|   `-- database-schema.md
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
- Backend: FastAPI, Pydantic, MongoDB, PyMongo
- Ingestion: OpenAI-powered upload extraction and website-to-menu structuring
- Recommendations: OpenAI-generated ranking guided by user profile, menu content, and estimated nutrition

## Backend setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python -m app.init_db
uvicorn app.main:app --reload
```

API runs at `http://localhost:8000`, Swagger at `http://localhost:8000/docs`.

The backend expects MongoDB to be available at the `MONGODB_URL` in [backend/.env.example](/c:/Users/Projects/HealthyBite/backend/.env.example). The default is `mongodb://localhost:27017` with database name `platewise`.
Set `OPENAI_API_KEY` in [backend/.env.example](/c:/Users/Projects/HealthyBite/backend/.env.example) before using upload analysis, URL ingestion, or recommendations.

## Frontend setup

```bash
cd frontend
npm install
copy .env.example .env.local
npm run dev
```

Frontend runs at `http://localhost:3000`.

## Daily run commands

Use 2 terminals.

Backend terminal from [backend](/c:/Users/Projects/HealthyBite/backend):

```powershell
cd c:\Users\Projects\HealthyBite\backend
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Frontend terminal from [frontend](/c:/Users/Projects/HealthyBite/frontend):

```powershell
cd c:\Users\Projects\HealthyBite\frontend
npm run dev
```

If dependencies are not installed yet, run these once first.

Backend first-time install:

```powershell
cd c:\Users\Projects\HealthyBite\backend
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Frontend first-time install:

```powershell
cd c:\Users\Projects\HealthyBite\frontend
npm install
```

Required backend env values in [backend/.env](/c:/Users/Projects/HealthyBite/backend/.env):

```env
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=platewise
OPENAI_API_KEY=your_openai_key_here
OPENAI_MENU_MODEL=gpt-4.1
OPENAI_RECOMMENDATION_MODEL=gpt-4.1
OPENAI_ENABLE_WEB_SEARCH=true
```

Required frontend env value in [frontend/.env.local](/c:/Users/Projects/HealthyBite/frontend/.env.local):

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api
```

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
- `GET /api/menus`
- `GET /api/menus/{menu_id}`
- `POST /api/recommendations/{menu_id}`
- `GET /api/history`
- `PUT /api/history/{recommendation_id}/save`

Detailed request and response notes are in [docs/api.md](/c:/Users/Projects/HealthyBite/docs/api.md).

## Notes on estimation and safety

- Nutrition values are estimated from menu wording, model inference, and optional web lookup support.
- Allergens are inferred from menu information and should be treated as warnings, not guarantees.
- The system avoids medical claims and uses cautious wording throughout the API and UI.
- The system is a food guidance tool, not a clinician, and should not be used as medical advice.

## Sample parser assets

- Upload parser sample: [backend/sample_data/sample_menu_upload.txt](/c:/Users/Projects/HealthyBite/backend/sample_data/sample_menu_upload.txt)
- Website parser sample payload: [backend/sample_data/sample_restaurant_payload.json](/c:/Users/Projects/HealthyBite/backend/sample_data/sample_restaurant_payload.json)

## Suggested next improvements

- Replace demo header auth with JWT bearer auth on protected routes.
- Add background jobs for OCR/crawling.
- Swap placeholder nutrition inference for a stronger ingredient knowledge base or model-assisted extraction.
- Add file persistence, S3 support, and OCR providers for production use.
