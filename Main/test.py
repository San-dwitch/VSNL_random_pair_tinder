import csv
import re
with open(r'..\data\vsnl.csv') as f:
    dt = csv.DictReader(f)
    for person in dt:
        age = 2021 - int((re.findall('\d{4}', person['Date of birth']))[0])  # compute age
        print(age)