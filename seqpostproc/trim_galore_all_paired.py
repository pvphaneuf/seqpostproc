#! /usr/bin/env python


import subprocess
import os
import collections
import sys
import getopt


# This and AutoBreseq re-use the same functions and could be combined
# into one package.


SAMPLE_FILE_EXTENSION = ".fastq"
SAMPLE_NAME_DELIMITER = "_S"
FIND_SUBSTRING_FAILURE = -1

TRIM_GALORE_CMD = "~/TrimGalore-0.4.3/trim_galore"
EXECUTE_FASTQC_OPTION = "--fastqc"
PAIRED_READ_OPTION = "--paired"
BASE_QUALITY_CUTOFF_OPTION = "-q"
BASE_QUAILTY_CUTOFF = 20
PATH_TO_CUTADAPT_OPTION = "--path_to_cutadapt"
PATH_TO_CUTADAPT = "~/.local/bin/cutadapt"
READ_1_ADAPTER_OPTION = "-a"
READ_1_ADAPTER = "AGATCGGAAGAGCACACGTCTGAACTCCAGTCA"
READ_2_ADAPTER_OPTION = "-a2"
READ_2_ADAPTER = "AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGT"
READ_1_SUBSTR = "_R1_001.fastq"
READ_2_SUBSTR = "_R2_001.fastq"


__author__ = 'Patrick Phaneuf'


def main():

    local_file_list = get_local_file_list()

    sample_file_dict = get_sample_file_dict(local_file_list)

    for key in sample_file_dict.keys():
        cmd_list = get_trim_galore_cmd(sample_file_dict[key])
        cmd_str = trim_galore_cmd_list_to_string(cmd_list)

        # Python documentation warned that there are security risks with using
        # shell=True for shell injection.
        subprocess.call(cmd_str, shell=True)


# TODO: Write unit test for trim_galore_cmd_list_to_string function.
def trim_galore_cmd_list_to_string(cmd_list):

    return ' '.join(cmd_list)


def get_trim_galore_cmd(sample_read_file_list):

    for read_file_name in sample_read_file_list:
        if READ_1_SUBSTR in read_file_name:
            read_1 = read_file_name
        elif READ_2_SUBSTR in read_file_name:
            read_2 = read_file_name

    trim_galore_cmd_list = [TRIM_GALORE_CMD,
                            EXECUTE_FASTQC_OPTION,
                            PAIRED_READ_OPTION,
                            BASE_QUALITY_CUTOFF_OPTION,
                            str(BASE_QUAILTY_CUTOFF),
                            PATH_TO_CUTADAPT_OPTION,
                            PATH_TO_CUTADAPT,
                            READ_1_ADAPTER_OPTION,
                            READ_1_ADAPTER,
                            READ_2_ADAPTER_OPTION,
                            READ_2_ADAPTER,
                            read_1,
                            read_2]

    return trim_galore_cmd_list


def get_local_file_list():

    local_file_list = []

    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for f in files:
        local_file_list.append(f)

    return local_file_list


def get_sample_file_dict(local_file_list):

    sample_file_list = get_local_sample_file_list(local_file_list)

    sample_list = get_local_samples(local_file_list)

    sample_file_dict = collections.defaultdict(list)

    for sample in sample_list:

        # appending SAMPLE_NAME_DELIMITER ("_S") to the end of a sample name since asdf_1_S1.fastq will include
        # asdf_10_S1.fastq as an additional sample file if there are no delimiters after the sample value.
        sample_name_with_delimiter = sample + SAMPLE_NAME_DELIMITER

        for sample_file in sample_file_list:

            if sample_name_with_delimiter in sample_file:

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
        local_file_list.append(f)

    return local_file_list


def is_sample_file(file_name):

    ret_val = False

    if file_name.find(SAMPLE_FILE_EXTENSION) != FIND_SUBSTRING_FAILURE:
        ret_val = True

    return ret_val


if __name__ == "__main__":
    main()
