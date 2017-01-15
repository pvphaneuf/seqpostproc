import subprocess

import os
import collections


SAMPLE_NAME_DELIMITER = "_S"
SAMPLE_FILE_EXTENSION = ".fastq"
FIND_SUBSTRING_FAILURE = -1


def get_sample_file_dict(local_file_list):

    sample_file_list = get_local_sample_file_list(local_file_list)

    sample_list = get_local_samples(local_file_list)

    sample_file_dict = collections.defaultdict(list)

    for sample in sample_list:
        for sample_file in sample_file_list:
            if sample in sample_file:
                sample_file_dict[sample].append(sample_file)

    return sample_file_dict


def get_local_samples(local_file_list):

    local_sample_file_list = get_local_sample_file_list(local_file_list)

    sample_list = []
    for local_sample in local_sample_file_list:
        sample_list.append(parse_sample_name(local_sample))

    unique_sample_list = remove_sample_duplicates(sample_list)

    return unique_sample_list


def parse_sample_name(file_name):

    sample_name_delimiter_index = file_name.find(SAMPLE_NAME_DELIMITER)

    sample_name = file_name[0:sample_name_delimiter_index]

    return sample_name


def remove_sample_duplicates(sample_file_list):

    ret_list = list(set(sample_file_list))

    return ret_list


def get_local_sample_file_list(local_file_list):

    local_sample_file_list = []

    for file_name in local_file_list:

        if is_sample_file(file_name):
            local_sample_file_list.append(file_name)

    return local_sample_file_list 


def get_local_file_list():

    local_file_list = []

    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for f in files:
        local_file_list.append(f                                   )

    return local_file_list


def is_sample_file(file_name):

    ret_val = False
  
    if file_name.find(SAMPLE_FILE_EXTENSION) != FIND_SUBSTRING_FAILURE:
        ret_val = True

    return ret_val



def main():

    local_file_list = get_local_file_list()

    sample_file_list = get_local_sample_file_list(local_file_list)

    cmd_prefix_str = "fastq_quality_trimmer -Q33 -v -t 20 -l 20"

    for sample_file in sample_file_list:

        trimmed_sample_name = "qtrim-" + sample_file

        cmd_str = cmd_prefix_str + " -i " + sample_file + " -o " + trimmed_sample_name

        subprocess.call(cmd_str, shell=True)

    
if __name__ == "__main__":
    main()
      
