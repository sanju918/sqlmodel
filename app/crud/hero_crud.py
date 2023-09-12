from app.models.hero import Hero
from app.sql_config import db, commit_rollback


async def create_heroes():
    hero_5 = Hero(name="pretest Naik", secret_name="lkdjfljdsljfd8lsdki", age=36, sex="Male")
    hero_4 = Hero(name="greentest Patel", secret_name="dkalkdfjiod", age=32, sex='Female')

    db.add(hero_5)
    db.add(hero_4)

    await commit_rollback()
