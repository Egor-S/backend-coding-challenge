import sys
import json
import argparse
from pathlib import Path

from sqlalchemy.orm import Session

sys.path.append(str((Path(__file__) / '..' / '..').resolve()))
from app import database, models, schemas


def create_or_update(db: Session, obj: models.Base, attrs=('id',)):
    q = db.query(type(obj)).filter_by(**{key: getattr(obj, key) for key in attrs}).first()
    if not q:
        db.add(obj)
        db.commit()
        db.refresh(obj)
    else:
        obj.id = q.id
        obj = db.merge(obj)
    return obj


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=Path, default='planning.json')
    args = parser.parse_args()

    models.Base.metadata.drop_all(bind=database.engine)
    models.Base.metadata.create_all(bind=database.engine)

    with args.input.open('r') as f:
        data = json.load(f)

    for i in data:
        full_entry = schemas.PlanningEntryOut(**i)
        talent = schemas.TalentIn(**i)
        manager = schemas.TalentIn(talentId=i['jobManagerId'], talentName=i['jobManagerName'])
        client = schemas.ClientIn(**i)
        entry = schemas.PlanningEntryIn(**i)

        with database.SessionLocal() as db:
            talent = models.Talent(id=talent.talentId, name=talent.talentName, grade=talent.talentGrade)
            if talent.id:
                talent = create_or_update(db, talent)

            manager = models.Talent(id=manager.talentId, name=manager.talentName)
            if manager.id:
                manager = create_or_update(db, manager)

            client = models.Client(id=client.clientId, name=client.clientName, industry=client.industry)
            client = create_or_update(db, client)

            entry = models.PlanningEntry(**schemas.PlanningEntryIn(**i).dict())
            for skill in full_entry.requiredSkills:
                skill = create_or_update(db, models.Skill(**skill.dict()), ('name', 'category'))
                entry.requiredSkills.append(skill)
            for skill in full_entry.optionalSkills:
                skill = create_or_update(db, models.Skill(**skill.dict()), ('name', 'category'))
                entry.optionalSkills.append(skill)

            db.add(entry)
            db.commit()


if __name__ == '__main__':
    main()
