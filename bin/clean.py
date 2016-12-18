import csv

# correct duplicate ids that exist in source csv
with open("Pokemon.csv", "r") as reader:
    csvreader = csv.reader(reader)
    print ','.join(next(csvreader))  # print header
    for i, row in enumerate(csvreader):
        print ",".join([str(i)] + row[1:])
