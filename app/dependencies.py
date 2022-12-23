from fastapi import Query

from .database import SessionLocal


class PaginationParams:
    def __init__(self, offset: int = Query(default=0, ge=0), limit: int = Query(default=100, ge=1, le=1000)):
        self.offset = offset
        self.limit = limit


class SortingParams:
    def __init__(self):
        pass


class SearchingParams:
    def __init__(self):
        pass


# from https://fastapi.tiangolo.com/tutorial/sql-databases/#create-a-dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
