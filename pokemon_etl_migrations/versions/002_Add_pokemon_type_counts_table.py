from migrate import *
from sqlalchemy import *
import datetime


meta = MetaData()

pokemon_type_counts = Table(
    'pokemon_type_counts', meta,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('type', String(256), unique=True),
    Column('type_1_count', Integer, default=0),
    Column('type_2_count', Integer, default=0),
    Column('created', DateTime),
    Column('updated', DateTime)
    )

def upgrade(migrate_engine):
    meta.bind = migrate_engine
    pokemon_type_counts.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    pokemon_type_counts.drop()
