# PlateWise API

Base URL: `http://localhost:8000/api`

Protected routes currently accept the `X-User-Id` header for the signed-in user.

## `POST /auth/signup`

Creates a new user account.

Request body:

```json
{
  "email": "user@example.com",
  "password": "strong-password"
}
```

Response:

```json
{
  "access_token": "jwt-token",
  "user_id": 1,
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
- Uses OpenAI to read the file and structure the menu
- Estimates likely ingredients, allergens, compatibility, and nutrition
- Stores structured menu items for recommendation ranking

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

Response includes the structured menu and AI-extracted items.

## `GET /menus`

Returns menus previously ingested by the current user, including enriched menu items.

## `GET /menus/{menu_id}`

Returns a single structured menu with its normalized items.

## `POST /recommendations/{menu_id}`

Builds recommendation results for a specific menu and the current user profile.
The backend uses OpenAI to rank dishes, explain the reasoning, and keep the wording cautious and non-medical.

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

The disclaimer always states that recommendations are estimated and not medical advice.

## `GET /history`

Returns saved recommendation history for the current user.

## `PUT /history/{recommendation_id}/save`

Marks a recommendation as saved or unsaved.

Request:

```json
{
  "saved": true
}
```
