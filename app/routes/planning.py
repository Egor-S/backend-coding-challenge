from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..dependencies import PaginationParams, SortingParams, get_db
from ..schemas import PlanningEntryOut, PlanningEntryModel, TalentModel, ClientModel
from ..models import PlanningEntry
from ..crud import get_planning_entries, paginate, sort_entries

router = APIRouter(prefix="/planning")


def flatten(obj: PlanningEntry) -> PlanningEntryOut:
    data = PlanningEntryModel.from_orm(obj).dict()
    if obj.talent:
        t = TalentModel.from_orm(obj.talent)
        data.update({'talentName': t.name, 'talentGrade': t.grade})
    if obj.jobManager:
        t = TalentModel.from_orm(obj.jobManager)
        data.update({'jobManagerName': t.name})
    c = ClientModel.from_orm(obj.client)
    data.update({'clientName': c.name, 'industry': c.industry})
    return PlanningEntryOut(**data)


@router.get("/", response_model=List[PlanningEntryOut])
def get(
        pagination: PaginationParams = Depends(),
        sorting: SortingParams = Depends(),
        db: Session = Depends(get_db)
):
    q = get_planning_entries(db)
    q = sort_entries(q, sorting)
    q = paginate(q, pagination)
    return [flatten(i) for i in q]
