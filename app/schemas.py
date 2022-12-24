from typing import Optional, List, Literal, Union, TypeVar, Generic
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, validator
from pydantic.generics import GenericModel


DATETIME_FORMAT = "%m/%d/%Y %I:%M %p"


class SkillEntry(BaseModel):
    name: str
    category: str

    class Config:
        orm_mode = True


# flaw: optional fields have default value. why: to achieve the same output, as original data
class PlanningEntryIn(BaseModel):
    id: int
    originalId: str
    talentId: str = ""
    bookingGrade: str = ""
    operatingUnit: str
    officeCity: str = ""
    officePostalCode: str
    jobManagerId: str = ""
    totalHours: float
    startDate: datetime
    endDate: datetime
    clientId: str
    isUnassigned: bool

    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime(DATETIME_FORMAT),
        }

    @validator('startDate', 'endDate', pre=True)
    def time_validate(cls, v):
        return datetime.strptime(v, DATETIME_FORMAT) if isinstance(v, str) else v


class TalentIn(BaseModel):
    talentId: str = ""
    talentName: str = ""
    talentGrade: str = ""


class ClientIn(BaseModel):
    clientId: str
    clientName: str = ""
    industry: str = ""


class PlanningEntryOut(PlanningEntryIn, TalentIn, ClientIn):
    jobManagerName: str = ""
    requiredSkills: Optional[List[SkillEntry]] = []
    optionalSkills: Optional[List[SkillEntry]] = []

    class Config(PlanningEntryIn.Config):
        orm_mode = True


class PlanningEntryModel(PlanningEntryIn):
    requiredSkills: Optional[List[SkillEntry]] = []
    optionalSkills: Optional[List[SkillEntry]] = []

    class Config(PlanningEntryIn.Config):
        orm_mode = True


class TalentModel(BaseModel):
    id: str = ""
    name: str = ""
    grade: str = ""

    class Config:
        orm_mode = True


class ClientModel(BaseModel):
    id: str
    name: str = ""
    industry: str = ""

    class Config:
        orm_mode = True


class Orders(Enum):
    asc = "asc"
    desc = "desc"


SortableColumns = Literal["id", "originalId", "talentId", "talentName", "talentGrade", "bookingGrade",
                          "operatingUnit", "officeCity", "officePostalCode", "jobManagerName", "jobManagerId",
                          "totalHours", "startDate", "endDate", "clientName", "clientId", "industry", "isUnassigned"]


class ColumnOrder(BaseModel):
    column: SortableColumns
    order: Orders


QueryOrValues = Union[str, List[str]]
RangeT = TypeVar('RangeT')


class Range(GenericModel, Generic[RangeT]):
    min: Optional[RangeT] = None
    max: Optional[RangeT] = None


class FilteringParams(BaseModel):
    id: Optional[List[int]] = None
    originalId: Optional[QueryOrValues] = None
    talentId: Optional[QueryOrValues] = None
    talentName: Optional[QueryOrValues] = None
    talentGrade: Optional[QueryOrValues] = None
    bookingGrade: Optional[QueryOrValues] = None
    operatingUnit: Optional[QueryOrValues] = None
    officeCity: Optional[QueryOrValues] = None
    officePostalCode: Optional[QueryOrValues] = None
    jobManagerId: Optional[QueryOrValues] = None
    jobManagerName: Optional[QueryOrValues] = None
    totalHours: Optional[Range[float]] = None
    startDate: Optional[Range[datetime]] = None
    endDate: Optional[Range[datetime]] = None  # doesn't support custom date format :(
    clientId: Optional[QueryOrValues] = None
    isUnassigned: Optional[List[bool]] = None
    # requiredSkills: Optional[List[SkillEntry]] = None
    # optionalSkills: Optional[List[SkillEntry]] = None
