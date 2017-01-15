#! /usr/bin/env python


import subprocess
import os
import collections
import sys
import getopt


__author__ = 'pphaneuf'


SAMPLE_NAME_DELIMITER = "_S"
REFERENCE_NAME_EXTENSION = ".gbk"
SAMPLE_FILE_EXTENSION = ".fastq"
FIND_SUBSTRING_FAILURE = -1

PROGRAM_NAME = "/home/pphaneuf/breseq/breseq-0.29.0-Linux-x86_64/bin/breseq"
POPULATION_FLAG = "-p"
REFERENCE_FLAG = "-r"
OUTPUT_FLAG = "-o"
CORE_USAGE_FLAG = "-j"
POPULATION_FILTERING_FLAG = "--polymorphism-frequency-cutoff"

CORES_TO_USE = 8
POPULATION_FILTERING_CUTOFF = 0.00


# TODO: Add command line arguments for making the run a backgroud process.
#       Essentially what is within exec_python_reseq_script_nohup.

def main(argv):

    # TODO: The code for parsing the files and sample names
    #       should be in its own module.

    reference = ""
    polymorphism_option = False

    try:
        opts, args = getopt.getopt(argv,
                                   "hpr:",
                                   ["help",
                                    "polymorphism",
                                    "reference="])

    except getopt.GetoptError as err:
        print(str(err))
        print_usage()
        sys.exit(2)

    for opt, arg in opts:

        if opt in ("-h", "--help"):
            print_usage()
            sys.exit()

        elif opt in ("-p", "--polymorphism"):
            polymorphism_option = True

        elif opt in ("-r", "--reference"):
            reference = arg

    # TODO: This is probably a bug. Need to exit if this condition is hit.
    if reference == "":
        print("A reference file is required")

    local_file_list = get_local_file_list()

    sample_file_dict = get_sample_file_dict(local_file_list)

    for key in sample_file_dict.keys():
        breseq_cmd_list = get_breseq_cmd(polymorphism_option,
                                         reference,
                                         key,
                                         sample_file_dict[key])
        breseq_cmd_str = breseq_cmd_list_to_string(breseq_cmd_list)

        # Python documentation warned that there are security risks with using
        # shell=True for shell injection.
        subprocess.call(breseq_cmd_str, shell=True)


def print_usage():

    print('AutoBreseq -p <polymorphism> -r <reference>')


# TODO: Write unit test for breseq_cmd_list_to_string function.
def breseq_cmd_list_to_string(breseq_cmd_list):

    return ' '.join(breseq_cmd_list)


# TODO: Should take a data structure argument that contains all of the global flags we're currently using within.
def get_breseq_cmd(polymorphism_option,
                   reference,
                   sample_name,
                   sample_read_files):

    output_option = OUTPUT_FLAG + " " + sample_name

    if polymorphism_option is True:
        breseq_cmd_list = [PROGRAM_NAME,
                           POPULATION_FLAG,
                           CORE_USAGE_FLAG + " " + str(CORES_TO_USE),
                           POPULATION_FILTERING_FLAG + " " + str(POPULATION_FILTERING_CUTOFF),
                           REFERENCE_FLAG + " " + reference,
                           output_option]
    else:
        breseq_cmd_list = [PROGRAM_NAME,
                           CORE_USAGE_FLAG + " " + str(CORES_TO_USE),
                           REFERENCE_FLAG + " " + reference,
                           output_option]

    for sample_read_file in sample_read_files:

        breseq_cmd_list.append(sample_read_file)

    return breseq_cmd_list


def get_reference_name(reference_file_name):

    reference_name_delimiter_index = reference_file_name.find(
        REFERENCE_NAME_EXTENSION)

    reference_file_name = reference_file_name[0:reference_name_delimiter_index]

    return reference_file_name


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
    main(sys.argv[1:])
