from sqlalchemy.orm import Session, Query, joinedload, aliased

from .models import PlanningEntry, Talent, Client
from .dependencies import PaginationParams, SortingParams
from .schemas import FilteringParams, Range


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


def get_column(name: str):
    if name.startswith('talent'):
        c = getattr(assigned_talent, camel_case_lstrip(name, 'talent'))
    elif name.startswith('jobManager'):
        c = getattr(job_manager, camel_case_lstrip(name, 'jobManager'))
    elif name.startswith('client'):
        c = getattr(Client, camel_case_lstrip(name, 'client'))
    elif name == 'industry':
        c = Client.industry
    # todo requiredSkills, optionalSkills
    else:
        c = getattr(PlanningEntry, name)
    return c


def sort_entries(q: Query, params: SortingParams) -> Query:
    if not params.columns:
        return q
    order_by = []
    for c in params.columns:
        v = get_column(c.column)
        v = getattr(v, c.order.value)  # asc or desc
        order_by.append(v())
    return q.order_by(*order_by)


def filter_entries(q: Query, params: FilteringParams) -> Query:
    filters = []
    fields = params.dict(exclude_unset=True)
    if not fields:
        return q
    print(params.schema())
    for field in fields:
        column = get_column(field)
        value = getattr(params, field)
        if isinstance(value, list):  # value from list
            filters.append(column.in_(value))
        elif isinstance(value, str):  # substring
            filters.append(column.like(f"%{value}%"))
        elif isinstance(value, Range):  # range
            if value.min is not None:
                filters.append(column >= value.min)
            if value.max is not None:
                filters.append(column <= value.max)
    return q.filter(*filters)
