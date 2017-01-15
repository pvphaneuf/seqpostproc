import sys
import os
import csv
import subprocess


# TODO: put fastqc in path
FASTQC_PATH = "/home/pphaneuf/FastQC/fastqc"
EXTRACT_FLAG = "--extract"
THREAD_COUNT_FLAG = "--threads"
TEST_RESULT_INDEX = 0
TEST_NAME_INDEX = 1
SAMPLE_NAME_INDEX = 2


def main(fastqs_path):
    _exec_fastqc(fastqs_path)
    _make_summary(fastqs_path)
    _cleanup(fastqs_path)


def _exec_fastqc(fastqs_path):
    fastq_file_list = []
    for file_name in os.listdir(fastqs_path):
        if file_name.endswith(".fastq"):
            fastq_file_list.append(fastqs_path+'/'+file_name)
    fastqc_thread_count = len(fastq_file_list)
    fastqc_cmd_list = [FASTQC_PATH,
                       EXTRACT_FLAG,
                       THREAD_COUNT_FLAG,
                       str(fastqc_thread_count)]
    fastqc_cmd_list = fastqc_cmd_list + fastq_file_list
    subprocess.run(fastqc_cmd_list)


def _make_summary(fastqs_path):
    output = []
    results_file_path = ""
    for file_name in os.listdir(fastqs_path):
        fastqc_path = fastqs_path+'/'+file_name
        if "_fastqc" in fastqc_path and os.path.isdir(fastqc_path):
            results_file_path = fastqc_path+'/'+"summary.txt"
            with open(results_file_path) as fastqc_results_file:
                output.append(_get_sample_results(fastqc_results_file))
    # Uses the last results file open to populate header of summary.
    with open(results_file_path) as fastqc_results_file:
        header = _get_output_header(fastqc_results_file)
        output.insert(0, header)
    _write_consolidated_results(fastqs_path, output)


def _write_consolidated_results(fastqs_path, output):
    consolidated_results_path = fastqs_path + '/' + "summary.csv"
    with open(consolidated_results_path, 'w', newline='') as consolidated_results:
        csv_writer = csv.writer(consolidated_results, delimiter=',',)
        for row in output:
            csv_writer.writerow(row)


def _get_sample_results(fastqc_results_file):
    sample_results = []
    csv_reader = csv.reader(fastqc_results_file, delimiter='\t')
    for row in csv_reader:
        if not row: continue
        else:
            if not sample_results:
                sample_results.append(row[SAMPLE_NAME_INDEX ])
            sample_results.append(row[TEST_RESULT_INDEX])
    return sample_results


def _get_output_header(fastqc_results_file):
    output_header = ["sample"]
    csv_reader = csv.reader(fastqc_results_file, delimiter='\t')
    for row in csv_reader:
        if not row: continue
        else: output_header.append(row[TEST_NAME_INDEX])
    return output_header


def _cleanup(fastqs_path):
    for file_name in os.listdir(fastqs_path):
        file_path = fastqs_path+'/'+file_name
        if file_name.endswith(".html"):
            subprocess.run(["rm", file_path])
        # only remove the uncompressed fastqc dirs.
        elif os.path.isdir(file_path) and "_fastqc" in file_path:
            subprocess.run(["rm", '-r', file_path])


if __name__ == '__main__':
    main(sys.argv[1])
