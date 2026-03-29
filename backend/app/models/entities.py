from datetime import datetime

from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))

    profile: Mapped["UserProfile"] = relationship(back_populates="user", uselist=False)
    recommendations: Mapped[list["Recommendation"]] = relationship(back_populates="user")
    uploads: Mapped[list["UploadRecord"]] = relationship(back_populates="user")


class UserProfile(TimestampMixin, Base):
    __tablename__ = "user_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    name: Mapped[str] = mapped_column(String(120))
    age: Mapped[int] = mapped_column(Integer)
    sex: Mapped[str] = mapped_column(String(50))
    height_cm: Mapped[float] = mapped_column(Float)
    weight_kg: Mapped[float] = mapped_column(Float)
    activity_level: Mapped[str] = mapped_column(String(50))
    primary_goal: Mapped[str] = mapped_column(String(50))
    diet_type: Mapped[str] = mapped_column(String(50), default="none")
    allergies: Mapped[list[str]] = mapped_column(JSON, default=list)
    disliked_foods: Mapped[list[str]] = mapped_column(JSON, default=list)
    spice_preference: Mapped[str] = mapped_column(String(50))
    budget_preference: Mapped[str] = mapped_column(String(50))
    preferred_cuisines: Mapped[list[str]] = mapped_column(JSON, default=list)

    user: Mapped["User"] = relationship(back_populates="profile")


class Restaurant(TimestampMixin, Base):
    __tablename__ = "restaurants"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    website_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    cuisine_tags: Mapped[list[str]] = mapped_column(JSON, default=list)
    source_type: Mapped[str] = mapped_column(String(50), default="url")

    menus: Mapped[list["Menu"]] = relationship(back_populates="restaurant")


class Menu(TimestampMixin, Base):
    __tablename__ = "menus"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    restaurant_id: Mapped[int | None] = mapped_column(ForeignKey("restaurants.id"), nullable=True)
    source_type: Mapped[str] = mapped_column(String(50))
    source_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    source_filename: Mapped[str | None] = mapped_column(String(255), nullable=True)
    extracted_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    structured_json: Mapped[dict] = mapped_column(JSON, default=dict)

    restaurant: Mapped["Restaurant"] = relationship(back_populates="menus")
    items: Mapped[list["MenuItem"]] = relationship(back_populates="menu")
    uploads: Mapped[list["UploadRecord"]] = relationship(back_populates="menu")


class MenuItem(TimestampMixin, Base):
    __tablename__ = "menu_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    menu_id: Mapped[int] = mapped_column(ForeignKey("menus.id"))
    category: Mapped[str | None] = mapped_column(String(100), nullable=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    price: Mapped[float | None] = mapped_column(Float, nullable=True)
    inferred_ingredients: Mapped[list[str]] = mapped_column(JSON, default=list)
    nutrition_estimate: Mapped[dict] = mapped_column(JSON, default=dict)
    allergens: Mapped[list[str]] = mapped_column(JSON, default=list)
    diet_compatibility: Mapped[list[str]] = mapped_column(JSON, default=list)
    confidence_score: Mapped[float] = mapped_column(Float, default=0.5)

    menu: Mapped["Menu"] = relationship(back_populates="items")
    recommendations: Mapped[list["Recommendation"]] = relationship(back_populates="menu_item")


class Recommendation(TimestampMixin, Base):
    __tablename__ = "recommendations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    menu_item_id: Mapped[int] = mapped_column(ForeignKey("menu_items.id"))
    recommendation_type: Mapped[str] = mapped_column(String(30), default="top_pick")
    match_score: Mapped[float] = mapped_column(Float)
    summary_reason: Mapped[str] = mapped_column(Text)
    why_recommended: Mapped[list[str]] = mapped_column(JSON, default=list)
    why_not_recommended: Mapped[list[str]] = mapped_column(JSON, default=list)
    warnings: Mapped[list[str]] = mapped_column(JSON, default=list)
    saved: Mapped[bool] = mapped_column(Boolean, default=False)

    user: Mapped["User"] = relationship(back_populates="recommendations")
    menu_item: Mapped["MenuItem"] = relationship(back_populates="recommendations")


class UploadRecord(TimestampMixin, Base):
    __tablename__ = "upload_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    menu_id: Mapped[int | None] = mapped_column(ForeignKey("menus.id"), nullable=True)
    file_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    file_type: Mapped[str] = mapped_column(String(50))
    source_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    processing_status: Mapped[str] = mapped_column(String(50), default="queued")
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    user: Mapped["User"] = relationship(back_populates="uploads")
    menu: Mapped["Menu"] = relationship(back_populates="uploads")

