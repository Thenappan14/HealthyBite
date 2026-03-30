from app.core.security import get_password_hash
from app.db.mongo import init_collections, next_sequence, with_timestamps
from app.db.session import database
from app.services.nutrition import enrich_menu_items


def seed() -> None:
    db = database
    init_collections(db)

    if db.users.find_one({"email": "demo@platewise.app"}):
        return

    user_id = next_sequence(db, "users")
    db.users.insert_one(
        with_timestamps(
            {
                "id": user_id,
                "email": "demo@platewise.app",
                "hashed_password": get_password_hash("demo1234"),
            }
        )
    )

    db.user_profiles.insert_one(
        with_timestamps(
            {
                "id": next_sequence(db, "user_profiles"),
                "user_id": user_id,
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
            }
        )
    )

    restaurant_id = next_sequence(db, "restaurants")
    db.restaurants.insert_one(
        with_timestamps(
            {
                "id": restaurant_id,
                "name": "Harbor Greens",
                "website_url": "https://example.com/harbor-greens",
                "cuisine_tags": ["healthy", "mediterranean"],
                "source_type": "seed",
            }
        )
    )

    raw_items = [
        {"category": "Bowls", "name": "Salmon Power Bowl", "description": "Brown rice, kale, avocado, edamame, sesame dressing", "price": 21},
        {"category": "Bowls", "name": "Chicken Fuel Bowl", "description": "Quinoa, broccoli, avocado, grilled chicken", "price": 18},
        {"category": "Pastas", "name": "Truffle Mushroom Pasta", "description": "Cream sauce, parmesan, garlic", "price": 19},
        {"category": "Dessert", "name": "Greek Yogurt Berry Parfait", "description": "Granola, berries, honey", "price": 9},
    ]

    menu_id = next_sequence(db, "menus")
    db.menus.insert_one(
        with_timestamps(
            {
                "id": menu_id,
                "restaurant_id": restaurant_id,
                "source_type": "seed",
                "source_url": "https://example.com/harbor-greens",
                "source_filename": None,
                "extracted_text": "Seeded sample menu",
                "structured_json": {"items": raw_items},
            }
        )
    )

    for item in enrich_menu_items(raw_items):
        db.menu_items.insert_one(
            with_timestamps(
                {
                    "id": next_sequence(db, "menu_items"),
                    "menu_id": menu_id,
                    "category": item["category"],
                    "name": item["name"],
                    "description": item["description"],
                    "price": item["price"],
                    "inferred_ingredients": item["inferred_ingredients"],
                    "nutrition_estimate": item["nutrition_estimate"],
                    "allergens": item["allergens"],
                    "diet_compatibility": item["diet_compatibility"],
                    "confidence_score": item["confidence_score"],
                }
            )
        )


if __name__ == "__main__":
    seed()
