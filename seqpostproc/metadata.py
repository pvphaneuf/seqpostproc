import os
import csv


def get_metadata_dict(file_path):
    metadata_dict = {}
    with open(file_path) as csv_file:
        metadata_reader = csv.reader(csv_file, delimiter=',')
        for row in metadata_reader:
            metadata_dict[row[0]] = row[1]
    return metadata_dict


def write_metadata_file(metadata_file_path, metadata_dict):
    with open(metadata_file_path, 'w') as f:
        w = csv.writer(f, metadata_dict.keys())
        for row in metadata_dict.items():
            w.writerow(row)


def get_metadata_file_name(metadata_dict):
    metdata_file_name = metadata_dict["ALE-number"]
    metdata_file_name += '_'+metadata_dict["Flask-number"]
    metdata_file_name += '_'+metadata_dict["Isolate-number"]
    metdata_file_name += '_'+metadata_dict["technical-replicate-number"]
    metdata_file_name += ".csv"
    return metdata_file_name


metadata_dir = "/data2/aledata/hug/metadata/"
for file_name in os.listdir(metadata_dir):
    if file_name[0] != '.' and (file_name.endswith(".csv") or file_name.endswith(".CSV")):
        file_path = metadata_dir+file_name
        metadata_dict = get_metadata_dict(file_path)
        metadata_dict["temperature"] = "37"
        metadata_file_name = get_metadata_file_name(metadata_dict)
        metadata_file_path = metadata_dir+metadata_file_name
        write_metadata_file(metadata_file_path, metadata_dict)
