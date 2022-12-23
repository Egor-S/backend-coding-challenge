from sqlalchemy import Boolean, Column, ForeignKey, Integer, Float, String, DateTime, UniqueConstraint, Table
from sqlalchemy.orm import relationship

from .database import Base


required_skills = Table(
    "required_skills", Base.metadata,
    Column("planning_entry_id", ForeignKey("planning_entries.id")),
    Column("skill_id", ForeignKey("skills.id")),
)
optional_skills = Table(
    "optional_skills", Base.metadata,
    Column("planning_entry_id", ForeignKey("planning_entries.id")),
    Column("skill_id", ForeignKey("skills.id")),
)


class PlanningEntry(Base):
    __tablename__ = "planning_entries"
    id = Column(Integer, primary_key=True, index=True)
    originalId = Column(String, unique=True, nullable=False, index=True)
    talentId = Column(String, ForeignKey('talents.id'))
    bookingGrade = Column(String)
    operatingUnit = Column(String, nullable=False)  # is it related to office or client?
    officeCity = Column(String)  # is it related to client or/and postal code?
    officePostalCode = Column(String, nullable=False)
    jobManagerId = Column(String, ForeignKey('talents.id'))
    totalHours = Column(Float, nullable=True)  # could compute as endDate - startDate?
    startDate = Column(DateTime, nullable=False)
    endDate = Column(DateTime, nullable=False)
    clientId = Column(String, ForeignKey('clients.id'))
    isUnassigned = Column(Boolean, nullable=False)  # could compute as talentId == None?

    talent = relationship('Talent', foreign_keys=[talentId])
    jobManager = relationship('Talent', foreign_keys=[jobManagerId])
    client = relationship('Client')

    requiredSkills = relationship('Skill', secondary=required_skills)
    optionalSkills = relationship('Skill', secondary=optional_skills)


class Talent(Base):
    __tablename__ = "talents"
    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    grade = Column(String)


class Client(Base):
    __tablename__ = "clients"
    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    industry = Column(String)


class Skill(Base):
    __tablename__ = "skills"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    __table_args__ = (UniqueConstraint('name', 'category', name='_name_category'),)
