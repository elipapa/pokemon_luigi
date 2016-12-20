from luigi.contrib import sqla
from sqlalchemy import Boolean, DateTime, Integer, String, text
import csv
import datetime
import luigi
import settings


class LoadPokemonTask(sqla.CopyToTable):
    """
    Add pokemon data from csv file
    """

    table = "pokemon_base"
    columns = [
        (['id', Integer], {"primary_key": True}),
        (['name', String(256)], {"unique": True}),
        (['type_1', String(256)], {}),
        (['type_2', String(256)], {"nullable":True}),
        (['total', Integer], {}),
        (['hp', Integer], {}),
        (['attack', Integer], {}),
        (['defense', Integer], {}),
        (['special_attack', Integer], {}),
        (['special_defense', Integer], {}),
        (['speed', Integer], {}),
        (['generation', Integer], {}),
        (['legendary', Boolean], {}),
        (['created', DateTime], {})
        ]

    connection_string = settings.pokemon.db_connection
    csv_file = settings.pokemon.csv_file

    def rows(self):

        pokemon = []
        with open(self.csv_file, "r") as reader:
            csvreader = csv.reader(reader)
            next(csvreader)  # first line is header

            for row in csvreader:
                yield [unicode(col, 'utf-8') for col in row] \
                    + [datetime.datetime.utcnow()]


class PokemonAddTypeCounts(luigi.Task):
    """
    Add counts for types
    """
    connection_string = settings.pokemon.db_connection
    table = 'pokemon_type_counts'


    def requires(self):
        return LoadPokemonTask()

    def output(self):
        return sqla.SQLAlchemyTarget(
            self.connection_string, self.table, self.task_id)

    def run(self):
        last_run = self._get_last_run()
        types_rs = self._get_types_since_last_run(last_run)

        type_1s = {}
        type_2s = {}
        for row in types_rs:
            type_1, type_2 = row
            type_1s.setdefault(type_1, 0)
            type_1s[type_1] += 1
            if type_2:  # optional
                type_2s.setdefault(type_2, 0)
                type_2s[type_2] += 1

        for t in set(type_1s.keys() + type_2s.keys()):
            if self._type_exists(t):
                self._type_update(t, type_1s[t], type_2s.get(t, 0))
            else:
                self._type_insert(t, type_1s[t], type_2s.get(t, 0))


    def _get_types_since_last_run(self, last_run):
        """return result set of pokemon types since last run"""
        sql = "SELECT type_1, type_2 FROM pokemon_base"
        args = {}
        if last_run:
            sql += " WHERE :created < created"
            args = {'created': last_run}

        conn = self.output().engine.connect()
        return conn.execute(sql, args)

    def _get_last_run(self):
        conn = self.output().engine.connect()
        rs = conn.execute('SELECT MAX(updated) FROM pokemon_type_counts')
        max_updated = rs.fetchone()[0]
        # TODO standardize datetime formats
        return datetime.datetime.strptime(max_updated, '%Y-%m-%d %H:%M:%S.%f') \
            if max_updated else None

    def _type_exists(self, t):
        conn = self.output().engine.connect()
        rs = conn.execute(
            'SELECT COUNT(1) FROM pokemon_type_counts WHERE type=:type',
            {"type": t})
        return 0 < rs.fetchone()[0]

    def _type_update(self, t, type_1_count, type_2_count):
        conn = self.output().engine.connect()
        conn.execute(
            'UPDATE pokemon_type_counts SET type_1_count=:type_1_count, type_2_count=:type_2_count, updated=:updated WHERE type=:type',
            {"type_1_count": type_1_count, "type_2_count": type_2_count,
            "updated": datetime.datetime.utcnow(), "type": t})

    def _type_insert(self, t, type_1_count, type_2_count):
        conn = self.output().engine.connect()
        conn.execute(
            'INSERT INTO pokemon_type_counts (type, type_1_count, type_2_count, created, updated) VALUES (:type, :type_1_count, :type_2_count, :created, :updated)',
            {"type": t, "type_1_count": type_1_count, "type_2_count": type_2_count,
            "created": datetime.datetime.utcnow(), "updated": datetime.datetime.utcnow()})
