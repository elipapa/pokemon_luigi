from sqlalchemy import *
from migrate import *

meta = MetaData()

pokemon_base = Table(
    'pokemon_base', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String(256), unique=True),
    Column('type_1', String(256)),
    Column('type_2', String(256), nullable=True),
    Column('total', Integer),
    Column('hp', Integer),
    Column('attack', Integer),
    Column('defense', Integer),
    Column('special_attack', Integer),
    Column('special_defense', Integer),
    Column('speed', Integer),
    Column('generation', Integer),
    Column('legendary', Boolean),
    Column('created', DateTime)
    )


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    pokemon_base.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    pokemon_base.drop()
