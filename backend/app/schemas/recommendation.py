from pydantic import BaseModel


class RecommendationResult(BaseModel):
    menu_item_id: int
    dish_name: str
    category: str | None = None
    price: float | None = None
    source_page: int | None = None
    source_text: str | None = None
    match_score: float
    summary_reason: str
    nutrition_estimate: dict
    allergens: list[str]
    warnings: list[str]
    why_recommended: list[str]
    why_not_recommended: list[str]
    recommendation_type: str


class RecommendationResponse(BaseModel):
    disclaimer: str
    top_recommendations: list[RecommendationResult]
    alternatives: list[RecommendationResult]
    dishes_to_avoid: list[RecommendationResult]


class RecommendationHistoryItem(BaseModel):
    id: int
    type: str
    score: float
    dish_name: str
    summary_reason: str
    warnings: list[str]
    saved: bool
    created_at: str


class RecommendationSaveRequest(BaseModel):
    saved: bool
