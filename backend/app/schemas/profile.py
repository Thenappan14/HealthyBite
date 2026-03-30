from pydantic import BaseModel, Field


class UserProfileBase(BaseModel):
    name: str
    age: int = Field(ge=13, le=120)
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


class UserProfileCreate(UserProfileBase):
    user_id: int | None = None


class UserProfileRead(UserProfileBase):
    id: int
    user_id: int

    model_config = {"from_attributes": True}
