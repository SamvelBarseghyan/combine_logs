"""
Soultion:
    Algorithm:
        Step 1: I'm taking the whole content of whole log files:
        Step 2: I'm keeping them in a list with tuples(timestamp, data):
                F.e
                [("2018-01-07 12:40:30.475", "INFO ..."), ..., ("2018-01-08 16:28:15.129", "ERROR ...")]
        Step 3: Adding parsed with tuples content of files to one list
        Step 4: Sorting list with first element of tuple-> timestamp (comparing as string or as datetime)
        Step 5: Iterating from that list and witing line by line into new file
    Advantages of the algorithm over the first algorithm:
        Time
    Disadvantages of the algorithm over the first algorithm:
        Memory
"""
# For handling argument passed to script
import sys

# For handling duration and memory usage of script
import time
import tracemalloc

# For parsing content of the directory
from os import listdir
from os.path import isfile, join


def get_list_of_files(path_to_dir: str):
    """
    Function returns list of file names that directory contains.

    :param path_to_dir: path to directory of log files
    :type path_to_dir: str
    :return: list of file names
    """
    return [f for f in listdir(path_to_dir) if isfile(join(path_to_dir, f))]


if __name__ == '__main__':
    start_time = time.time()
    tracemalloc.start()

    list_of_arguments = sys.argv

    try:
        path_to_logs_directory = list_of_arguments[1]
    except IndexError as err:
        path_to_logs_directory = '../logs'

    log_file_names = get_list_of_files(path_to_logs_directory)
    res = list()
    for name in log_file_names:
        with open('/'.join(['../logs', name]), 'r') as file_:
            res1 = list()
            content = file_.readlines()
            for line in content:
                line = line.split(' ')
                res1.append((' '.join(line[:2]), ' '.join(line[2:])))
            res.extend(res1)
    res.sort(key=lambda x: x[0])
    with open('combined_logs_file.log', 'w') as f:
        for line in res:
            f.write(' '.join(line))
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
    print("Duration of script: ", str(end_time - start_time))
    tracemalloc.stop()
