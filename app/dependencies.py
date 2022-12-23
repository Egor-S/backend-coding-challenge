from typing import List, Optional
from fastapi import Query, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError

from .database import SessionLocal
from .schemas import ColumnOrder


class PaginationParams:
    def __init__(self, offset: int = Query(default=0, ge=0), limit: int = Query(default=100, ge=1, le=1000)):
        self.offset = offset
        self.limit = limit


class SortingParams:
    def __init__(self, sort: Optional[List[str]] = Query(
        default=None, example="talentId desc"
    )):
        self.columns: List[ColumnOrder] = []
        if not sort:
            return
        try:
            for v in sort:
                tokens = v.split()
                if len(tokens) != 2:  # dirty hack
                    tokens = (tokens + ['', ''])[:2]
                c, o = tokens
                self.columns.append(ColumnOrder(column=c, order=o))
        except ValidationError as e:
            raise HTTPException(status_code=422, detail=jsonable_encoder(e.errors()))


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
