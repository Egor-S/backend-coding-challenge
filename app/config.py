from pathlib import Path


app_root = Path(__file__).parent.resolve()
SQLALCHEMY_DATABASE_URL = f"sqlite:///{(app_root.parent / 'database.sqlite').resolve()}"
