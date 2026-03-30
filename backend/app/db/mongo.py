from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pymongo import ASCENDING, ReturnDocument
from pymongo.database import Database


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def with_timestamps(payload: dict[str, Any], *, update: bool = False) -> dict[str, Any]:
    now = utcnow()
    document = {**payload, "updated_at": now}
    if not update and "created_at" not in document:
        document["created_at"] = now
    return document


def next_sequence(db: Database, counter_name: str) -> int:
    record = db.counters.find_one_and_update(
        {"_id": counter_name},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    return int(record["seq"])


def init_collections(db: Database) -> None:
    db.users.create_index([("id", ASCENDING)], unique=True)
    db.users.create_index([("email", ASCENDING)], unique=True)
    db.user_profiles.create_index([("id", ASCENDING)], unique=True)
    db.user_profiles.create_index([("user_id", ASCENDING)], unique=True)
    db.restaurants.create_index([("id", ASCENDING)], unique=True)
    db.menus.create_index([("id", ASCENDING)], unique=True)
    db.menu_items.create_index([("id", ASCENDING)], unique=True)
    db.menu_items.create_index([("menu_id", ASCENDING)])
    db.recommendations.create_index([("id", ASCENDING)], unique=True)
    db.recommendations.create_index([("user_id", ASCENDING), ("created_at", ASCENDING)])
    db.upload_records.create_index([("id", ASCENDING)], unique=True)
    db.upload_records.create_index([("user_id", ASCENDING), ("created_at", ASCENDING)])


def strip_mongo_id(document: dict[str, Any] | None) -> dict[str, Any] | None:
    if not document:
        return None
    cleaned = dict(document)
    cleaned.pop("_id", None)
    return cleaned
