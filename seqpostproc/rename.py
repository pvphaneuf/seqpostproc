import os


def main():
    for file_name in os.listdir('.'):
        if _is_breseq_report(file_name):
            serialization_str = _get_serialization_str(file_name)
            os.rename(file_name, serialization_str)


# TODO: future implementation, search for existence of /output/log.txt
def _is_breseq_report(file_name):
    return '_A' in file_name and '_F' in file_name and '_I' in file_name and '_R' in file_name


def _get_serialization_str(file_name):
    ALE_num = find_between(file_name, "_A", "_F")
    flask_num = find_between(file_name, "_F", "_I")
    isolate_num = find_between(file_name, "_I", "_R")
    try:
        replicate_num = file_name[file_name.index("_R")+len("_R"):]
    except ValueError:
        replicate_num = ""
    return ALE_num+'-'+flask_num+'-'+isolate_num+'-'+replicate_num


def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


if __name__ == '__main__':
    main()
