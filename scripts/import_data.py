import sys
import json
import argparse
from pathlib import Path

sys.path.append(str((Path(__file__) / '..' / '..').resolve()))
from app import database, models, schemas


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=Path, default='planning.json')
    args = parser.parse_args()

    models.Base.metadata.drop_all(bind=database.engine)
    models.Base.metadata.create_all(bind=database.engine)

    with args.input.open('r') as f:
        data = json.load(f)

    clients = {}
    talents = {}
    skills = {}
    planning_entries = []

    db = database.SessionLocal()
    for i in data:
        full_entry = schemas.PlanningEntryOut(**i)
        talent = schemas.TalentIn(**i)
        manager = schemas.TalentIn(talentId=i['jobManagerId'], talentName=i['jobManagerName'])
        client = schemas.ClientIn(**i)
        entry = schemas.PlanningEntryIn(**i)

        for t in (talent, manager):
            if not t.talentId:
                continue
            t2 = talents.get(t.talentId, None)
            if t2 is None:
                talents[t.talentId] = models.Talent(id=t.talentId, name=t.talentName, grade=t.talentGrade)
            elif not t2.grade:
                t2.grade = t.talentGrade

        if client.clientId not in clients:
            clients[client.clientId] = models.Client(
                id=client.clientId, name=client.clientName, industry=client.industry
            )

        entry = models.PlanningEntry(**entry.dict())
        planning_entries.append(entry)

        for skill_type in ('requiredSkills', 'optionalSkills'):
            target_list = getattr(entry, skill_type)
            for skill in getattr(full_entry, skill_type):
                key = (skill.name, skill.category)
                if key not in skills:
                    skills[key] = models.Skill(**skill.dict())
                target_list.append(skills[key])

    db.add_all(talents.values())
    db.add_all(clients.values())
    db.add_all(skills.values())
    db.add_all(planning_entries)
    db.commit()
    db.close()


if __name__ == '__main__':
    main()
