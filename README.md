# pokemon_luigi
Example ETL pipeline task using luigi

### Install
```shell
> virtualenv pokemon_luigi.env
> source pokemon_luigi.env/bin/activate
> pip install -r requirements.txt
# create sqlite database
> python manage.py version_control
> python manage.py upgrade
```

### Usage
```shell
# run the luigi task
# PYTHONPATH is required as luigi only uses modules in the global path
> PYTHONPATH=. luigi --local-scheduler --module pokemon_etl PokemonAddTypeCounts
# verify the results in the db
> sqlite3 -csv -batch pokemon.db "SELECT * FROM pokemon_type_counts ORDER BY type_1_count DESC"
```
