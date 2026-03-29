# PlateWise API

Base URL: `http://localhost:8000/api`

Demo protected routes accept the `X-User-Id` header.

## `POST /auth/signup`

Creates a new user account.

Request body:

```json
{
  "email": "demo@platewise.app",
  "password": "demo1234"
}
```

Response:

```json
{
  "access_token": "jwt-token",
  "token_type": "bearer"
}
```

## `POST /auth/login`

Authenticates an existing user.

## `GET /profile`

Returns the current user's profile or `null` if setup is incomplete.

## `PUT /profile`

Upserts the current user's profile.

Important fields:

- `primary_goal`: `fat_loss | muscle_gain | maintenance | better_energy | balanced_eating`
- `diet_type`: `none | vegetarian | vegan | halal | pescatarian | lactose_free | gluten_free`
- `allergies`: string array
- `disliked_foods`: string array
- `preferred_cuisines`: string array

## `POST /uploads`

Multipart form upload for menu files.

- Accepts: `.jpg`, `.jpeg`, `.png`, `.webp`, `.pdf`
- Extracts OCR text
- Parses categories, dishes, descriptions, and prices
- Enriches dishes with estimated nutrition and compatibility data

Response shape:

```json
{
  "upload_id": 1,
  "menu_id": 1,
  "extracted_preview": "Sample OCR extraction..."
}
```

## `POST /ingest/url`

Request:

```json
{
  "url": "https://example.com/menu"
}
```

Response includes the structured menu and enriched items.

## `POST /recommendations/{menu_id}`

Builds recommendation results for a specific menu and the current user profile.

Response includes:

- `top_recommendations`
- `alternatives`
- `dishes_to_avoid`
- `disclaimer`

Each result contains:

- `match_score`
- `summary_reason`
- `nutrition_estimate`
- `allergens`
- `warnings`
- `why_recommended`
- `why_not_recommended`

## `GET /history`

Returns saved recommendation history for the current user.

