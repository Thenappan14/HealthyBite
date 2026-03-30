from app.db.mongo import init_collections
from app.db.session import database


def seed() -> None:
    init_collections(database)


if __name__ == "__main__":
    seed()
