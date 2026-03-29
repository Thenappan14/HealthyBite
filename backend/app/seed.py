from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models import Menu, MenuItem, Restaurant, User, UserProfile
from app.services.nutrition import enrich_menu_items


def seed() -> None:
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    if db.query(User).filter(User.email == "demo@platewise.app").first():
        db.close()
        return

    user = User(email="demo@platewise.app", hashed_password=get_password_hash("demo1234"))
    db.add(user)
    db.flush()

    profile = UserProfile(
        user_id=user.id,
        name="Jordan Lee",
        age=31,
        sex="female",
        height_cm=168,
        weight_kg=64,
        activity_level="moderately_active",
        primary_goal="better_energy",
        diet_type="pescatarian",
        allergies=["peanuts"],
        disliked_foods=["mushroom"],
        spice_preference="medium",
        budget_preference="moderate",
        preferred_cuisines=["mediterranean", "japanese"],
    )
    db.add(profile)

    restaurant = Restaurant(
        name="Harbor Greens",
        website_url="https://example.com/harbor-greens",
        cuisine_tags=["healthy", "mediterranean"],
        source_type="seed",
    )
    db.add(restaurant)
    db.flush()

    raw_items = [
        {"category": "Bowls", "name": "Salmon Power Bowl", "description": "Brown rice, kale, avocado, edamame, sesame dressing", "price": 21},
        {"category": "Bowls", "name": "Chicken Fuel Bowl", "description": "Quinoa, broccoli, avocado, grilled chicken", "price": 18},
        {"category": "Pastas", "name": "Truffle Mushroom Pasta", "description": "Cream sauce, parmesan, garlic", "price": 19},
        {"category": "Dessert", "name": "Greek Yogurt Berry Parfait", "description": "Granola, berries, honey", "price": 9},
    ]

    menu = Menu(
        restaurant_id=restaurant.id,
        source_type="seed",
        source_url=restaurant.website_url,
        extracted_text="Seeded sample menu",
        structured_json={"items": raw_items},
    )
    db.add(menu)
    db.flush()

    for item in enrich_menu_items(raw_items):
        db.add(
            MenuItem(
                menu_id=menu.id,
                category=item["category"],
                name=item["name"],
                description=item["description"],
                price=item["price"],
                inferred_ingredients=item["inferred_ingredients"],
                nutrition_estimate=item["nutrition_estimate"],
                allergens=item["allergens"],
                diet_compatibility=item["diet_compatibility"],
                confidence_score=item["confidence_score"],
            )
        )

    db.commit()
    db.close()


if __name__ == "__main__":
    seed()

