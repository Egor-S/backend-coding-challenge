from sqlalchemy.orm import Session, Query, joinedload, aliased

from .models import PlanningEntry, Talent, Client
from .dependencies import PaginationParams, SortingParams


assigned_talent = aliased(Talent)
job_manager = aliased(Talent)


def get_planning_entries(db: Session) -> Query:
    return db.query(PlanningEntry)\
        .join(assigned_talent, PlanningEntry.talent, isouter=True)\
        .join(job_manager, PlanningEntry.jobManager, isouter=True)\
        .join(Client)\
        .options(joinedload('*'))


def paginate(q: Query, params: PaginationParams) -> Query:
    return q.offset(params.offset).limit(params.limit)


def camel_case_lstrip(s: str, prefix: str):
    s = s.lstrip(prefix)
    return s[:1].lower() + s[1:]


def sort_entries(q: Query, params: SortingParams) -> Query:
    if not params.columns:
        return q
    order_by = []
    for c in params.columns:
        if c.column.startswith('talent'):
            v = getattr(assigned_talent, camel_case_lstrip(c.column, 'talent'))
        elif c.column.startswith('jobManager'):
            v = getattr(job_manager, camel_case_lstrip(c.column, 'jobManager'))
        elif c.column.startswith('client'):
            v = getattr(Client, camel_case_lstrip(c.column, 'client'))
        elif c.column == 'industry':
            v = Client.industry
        else:
            v = getattr(PlanningEntry, c.column)
        v = getattr(v, c.order.value)  # asc or desc
        order_by.append(v())
    return q.order_by(*order_by)
