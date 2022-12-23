from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel


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
    startDate: datetime  # todo set right format
    endDate: datetime
    clientId: str
    isUnassigned: bool


class PlanningEntryOut(PlanningEntryIn):
    talentName: str = ""
    talentGrade: str = ""
    jobManagerName: str = ""
    clientName: str = ""
    industry: str = ""
    requiredSkills: Optional[List[SkillEntry]] = []
    optionalSkills: Optional[List[SkillEntry]] = []
