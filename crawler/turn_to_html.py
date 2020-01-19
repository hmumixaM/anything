import csv

filename = "/Users/max/Desktop/gif.csv"
with open(filename) as f:
    reader = csv.reader(f)
    row = list(next(reader))
    for i in row:
        print(i)