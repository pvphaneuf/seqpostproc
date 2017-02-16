import os
import csv

# Expecting a CSV with each line as: #,#,#,#,current_name
with open("mapping.csv") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        new_dir_name = row[0]+'-'+row[1]+'-'+row[2]+'-'+row[3]
        os.rename(row[4],new_dir_name)
