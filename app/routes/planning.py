from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..dependencies import PaginationParams, SortingParams, get_db
from ..schemas import PlanningEntryOut

router = APIRouter(prefix="/planning")


@router.get("/", response_model=List[PlanningEntryOut])
def get(
        pagination: PaginationParams = Depends(),
        sorting: SortingParams = Depends(),
        db: Session = Depends(get_db)
):
    return []
