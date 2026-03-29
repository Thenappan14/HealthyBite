# PlateWise Architecture

## Overview

PlateWise is organized as a small monorepo with a Next.js frontend and a FastAPI backend.

- `frontend/` renders the product UI, profile forms, upload interactions, URL ingestion flow, results cards, and saved history.
- `backend/` exposes REST APIs for auth, profiles, uploads, URL crawling, menu normalization, nutrition estimation, recommendation ranking, and history.
- `docs/` captures architecture, API contracts, and a SQL-oriented schema reference.

## Backend flow

1. A user creates or updates a profile.
2. A menu is ingested from either:
   - an uploaded image or PDF through the OCR placeholder service
   - a restaurant website URL through the heuristic crawler
3. Parsed menu lines are normalized into structured menu items.
4. Each menu item is enriched with:
   - inferred ingredients
   - estimated macros and sodium
   - likely allergens
   - diet compatibility
   - confidence score
5. The recommendation engine applies:
   - hard filters for allergy conflicts and strict diet conflicts
   - soft scoring for goals, protein, calories, sugar, sodium, fiber, vegetables, cuisine fit, budget, and confidence
6. Results are returned with explanations and saved to recommendation history.

## Frontend flow

- Landing page introduces the product.
- Auth pages provide entry points for signup and login.
- Profile page captures health goals, restrictions, and preferences.
- Dashboard summarizes recent activity and the user profile.
- Upload page supports drag-and-drop images and PDFs.
- URL page accepts restaurant websites for crawl-based ingestion.
- Results page shows top picks, alternatives, and dishes to avoid.
- Saved page shows previous recommendation history.

## Production-oriented extension points

- Replace the OCR placeholder with Tesseract, a vision API, or a document AI service.
- Replace heuristic crawling with a menu extractor that combines HTML parsing and model-assisted cleanup.
- Add background workers for ingestion and recommendation jobs.
- Replace header-based demo auth with JWT session management.
- Add automated tests, migrations, and observability.

