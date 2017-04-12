import os
import os.path
import csv

# Expecting a CSV with each line as: #,#,#,#,current_name
with open("mapping.csv") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        current_file_name = row[4]
        if os.path.isdir(current_file_name):
            new_dir_name = row[0]+'-'+row[1]+'-'+row[2]+'-'+row[3]
            os.rename(current_file_name,new_dir_name)
