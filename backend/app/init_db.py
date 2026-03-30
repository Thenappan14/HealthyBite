from app.db.mongo import init_collections
from app.db.session import database


def init_db() -> None:
    init_collections(database)


if __name__ == "__main__":
    init_db()
