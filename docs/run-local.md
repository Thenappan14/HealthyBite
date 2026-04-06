# Run PlateWise Locally

## Backend

Run these from [backend](/c:/Users/Projects/HealthyBite/backend):

```powershell
cd c:\Users\Projects\HealthyBite\backend
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Backend URLs:

- API: `http://127.0.0.1:8000`
- Swagger docs: `http://127.0.0.1:8000/docs`
- Health: `http://127.0.0.1:8000/health`

Your [backend/.env](/c:/Users/Projects/HealthyBite/backend/.env) should include:

```env
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=platewise
```

Local OCR notes:

- Text PDFs work through `pypdf`
- Images require Tesseract OCR installed locally
- Scanned PDFs require both Tesseract OCR and Poppler on Windows because `pdf2image` converts PDF pages into images before OCR

## Frontend

Run these from [frontend](/c:/Users/Projects/HealthyBite/frontend):

```powershell
cd c:\Users\Projects\HealthyBite\frontend
npm install
npm run dev
```

Frontend URL:

- App: `http://localhost:3000`

Your [frontend/.env.local](/c:/Users/Projects/HealthyBite/frontend/.env.local) should include:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api
```

## Normal daily workflow

Open 2 terminals:

1. Backend terminal

```powershell
cd c:\Users\Projects\HealthyBite\backend
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

2. Frontend terminal

```powershell
cd c:\Users\Projects\HealthyBite\frontend
npm run dev
```

## If backend packages break

Recreate the backend virtual environment:

```powershell
cd c:\Users\Projects\HealthyBite\backend
Remove-Item -Recurse -Force .venv
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```
