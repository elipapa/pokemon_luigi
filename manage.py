#!/usr/bin/env python
from migrate.versioning.shell import main

if __name__ == '__main__':
    main(url='sqlite:///pokemon.db', debug='False', repository='pokemon_etl_migrations')
