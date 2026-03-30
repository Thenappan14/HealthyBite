# PlateWise MongoDB Schema

PlateWise uses MongoDB collections with numeric application ids stored in an `id` field for API friendliness.

## Collections

### `users`

```json
{
  "id": 1,
  "email": "demo@platewise.app",
  "hashed_password": "...",
  "created_at": "2026-03-30T00:00:00Z",
  "updated_at": "2026-03-30T00:00:00Z"
}
```

### `user_profiles`

```json
{
  "id": 1,
  "user_id": 1,
  "name": "Jordan Lee",
  "age": 31,
  "sex": "female",
  "height_cm": 168,
  "weight_kg": 64,
  "activity_level": "moderately_active",
  "primary_goal": "better_energy",
  "diet_type": "pescatarian",
  "allergies": ["peanuts"],
  "disliked_foods": ["mushroom"],
  "spice_preference": "medium",
  "budget_preference": "moderate",
  "preferred_cuisines": ["mediterranean", "japanese"],
  "created_at": "2026-03-30T00:00:00Z",
  "updated_at": "2026-03-30T00:00:00Z"
}
```

### `restaurants`

```json
{
  "id": 1,
  "name": "Harbor Greens",
  "website_url": "https://example.com/harbor-greens",
  "cuisine_tags": ["healthy", "mediterranean"],
  "source_type": "url"
}
```

### `menus`

```json
{
  "id": 1,
  "restaurant_id": 1,
  "source_type": "upload",
  "source_url": null,
  "source_filename": "menu.pdf",
  "extracted_text": "...",
  "structured_json": {
    "items": []
  }
}
```

### `menu_items`

```json
{
  "id": 1,
  "menu_id": 1,
  "category": "Bowls",
  "name": "Salmon Power Bowl",
  "description": "Brown rice, kale, avocado, edamame, sesame dressing",
  "price": 21,
  "inferred_ingredients": ["salmon", "avocado"],
  "nutrition_estimate": {
    "calories": 410,
    "protein_g": 30,
    "carbs_g": 12,
    "fat_g": 18,
    "fiber_g": 4,
    "sugar_g": 4,
    "sodium_mg": 520
  },
  "allergens": ["fish", "sesame"],
  "diet_compatibility": ["none", "pescatarian"],
  "confidence_score": 0.85
}
```

### `recommendations`

```json
{
  "id": 1,
  "user_id": 1,
  "menu_item_id": 1,
  "recommendation_type": "top_pick",
  "match_score": 88.4,
  "summary_reason": "Looks supportive for steady energy with likely fiber and meal substance.",
  "why_recommended": [],
  "why_not_recommended": [],
  "warnings": [],
  "saved": false
}
```

### `upload_records`

```json
{
  "id": 1,
  "user_id": 1,
  "menu_id": 1,
  "file_name": "menu.pdf",
  "file_type": "pdf",
  "source_url": null,
  "processing_status": "completed",
  "notes": "Parsed with rule-based OCR placeholder pipeline."
}
```

### `counters`

```json
{
  "_id": "users",
  "seq": 1
}
```

The `counters` collection is used to generate sequential numeric ids for each main collection.
