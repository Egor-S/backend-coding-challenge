from sqlalchemy.orm import Session, Query, joinedload

from .models import PlanningEntry, Client, Talent
from .dependencies import PaginationParams


def get_planning_entries(db: Session) -> Query:
    return db.query(PlanningEntry).options(joinedload('*'))


def paginate(q: Query, params: PaginationParams) -> Query:
    return q.offset(params.offset).limit(params.limit)

