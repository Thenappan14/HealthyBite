from pydantic import BaseModel, Field, HttpUrl


class UploadResponse(BaseModel):
    upload_id: int
    menu_id: int
    extracted_preview: str


class UploadRecordRead(BaseModel):
    id: int
    user_id: int
    menu_id: int | None = None
    file_name: str | None = None
    file_type: str | None = None
    source_url: str | None = None
    processing_status: str
    notes: str | None = None
    file_path: str | None = None
    extracted_preview: str | None = None
    created_at: str
    updated_at: str


class UrlIngestRequest(BaseModel):
    url: HttpUrl


class MenuItemRead(BaseModel):
    id: int
    category: str | None = None
    name: str
    description: str | None = None
    price: float | None = None
    source_page: int | None = None
    source_text: str | None = None
    inferred_ingredients: list[str] = Field(default_factory=list)
    nutrition_estimate: dict = Field(default_factory=dict)
    allergens: list[str] = Field(default_factory=list)
    diet_compatibility: list[str] = Field(default_factory=list)
    confidence_score: float

    model_config = {"from_attributes": True}


class MenuRead(BaseModel):
    id: int
    source_type: str
    source_url: str | None = None
    source_filename: str | None = None
    extracted_text: str | None = None
    structured_json: dict
    items: list[MenuItemRead]

    model_config = {"from_attributes": True}
