from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel, validator


DATETIME_FORMAT = "%m/%d/%Y %I:%M %p"


class SkillEntry(BaseModel):
    name: str
    category: str


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
            datetime: lambda v: v.strformat(DATETIME_FORMAT),
        }

    @validator('startDate', 'endDate', pre=True)
    def time_validate(cls, v):
        return datetime.strptime(v, DATETIME_FORMAT)


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
