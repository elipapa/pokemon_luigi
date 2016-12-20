import luigi


class pokemon(luigi.Config):
    # TODO pull from credstash
    db_connection = luigi.Parameter(default="sqlite:///pokemon.db")
    csv_file = luigi.Parameter(default="datasets/pokemon_cleaned.csv")

pokemon().csv_file
pokemon().db_connection
