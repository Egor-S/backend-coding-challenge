from pathlib import Path
import sys

sys.path.append(str((Path(__file__) / '..' / '..').resolve()))
from app import database, models, config


def main():
    print(config.SQLALCHEMY_DATABASE_URL)


if __name__ == '__main__':
    main()
