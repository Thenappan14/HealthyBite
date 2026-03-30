from pydantic import BaseModel, Field


class UserProfileModel(BaseModel):
    id: int | None = None
    user_id: int
    name: str
    age: int
    sex: str
    height_cm: float
    weight_kg: float
    activity_level: str
    primary_goal: str
    diet_type: str = "none"
    allergies: list[str] = Field(default_factory=list)
    disliked_foods: list[str] = Field(default_factory=list)
    spice_preference: str
    budget_preference: str
    preferred_dining_styles: list[str] = Field(default_factory=list)
    preferred_cuisines: list[str] = Field(default_factory=list)


class MenuItemModel(BaseModel):
    id: int
    menu_id: int
    category: str | None = None
    name: str
    description: str | None = None
    price: float | None = None
    inferred_ingredients: list[str] = Field(default_factory=list)
    nutrition_estimate: dict = Field(default_factory=dict)
    allergens: list[str] = Field(default_factory=list)
    diet_compatibility: list[str] = Field(default_factory=list)
    confidence_score: float = 0.5
