#!/usr/bin/env python3
"""
Soultion:
    Algorithm:
        Step 1: I'm taking the whole list of log files and keeping pointer to them:
                F.e. if we have 7 files:
                [iter_file_1, iter_file_2 ... iter_file_7]
        Step 2: I'm creating list from their first lines
                F.e
                ["2018-01-07 12:40:30.475 INFO ...", ..., "2018-01-08 16:28:15.129 ERROR ..."]
        Step 3: As in the task it is given that content of whole log files are sorted
                I'm taking the lowest value with date-time and writing in a new file
        Step 4: I'm incrementing pointer in the file where I get the lowest timestamp.
        Step 5: Changing value in the "first lines" list
        Step 6: If pointer is refers to the end of file pop that pointer from the list of pointers
                and pop value from the list of the "first lines" list
        Step 7: Looping while the length of the list of pointers is not 0
    Advantages of the algorithm:
        Memory
    Disadvantages of the algorithm:
        Time
"""

# For handling argument passed to script
import sys

# For handling duration and memory usage of script
import time
import tracemalloc

# For parsing content of the directory
from os import listdir
from os.path import isfile, join

# For creating datetime obj from timestamps in log files for comparing
from datetime import datetime


def get_list_of_files(path_to_dir: str):
    """
    Function returns list of file names that directory contains.

    :param path_to_dir: path to directory of log files
    :type path_to_dir: str
    :return: list of file names
    """
    return [f for f in listdir(path_to_dir) if isfile(join(path_to_dir, f))]


def get_min_of_timestamps(lines: list):
    """
    Function is getting the "lowest"/"smallest" by date-time criteria element,
    and returns that and his index in list

    :param lines: list of lines that have been read from log files
    :type lines: list
    :return: element that contains "lowest" date-time and his index in list
    """
    # Note...
    #  Here we can use string to compare to timestamps but for security,
    #  so that there are no problems with comparing, I decided to use datetime objects

    min_index = 0
    min_element = lines[0]
    min_element_date = ' '.join(lines[0].split(' ')[:2])
    min_element_date = datetime.strptime(min_element_date, '%Y-%m-%d %H:%M:%S.%f')

    for i in range(1, len(lines)):
        if not lines[i]:
            continue
        min_el_date = ' '.join(lines[i].split(' ')[:2])
        element_date = datetime.strptime(min_el_date, '%Y-%m-%d %H:%M:%S.%f')
        if element_date < min_element_date:
            min_element = lines[i]
            min_index = i
            min_element_date = element_date
    return min_element, min_index


def get_next_line_of_file(pointer_list: list, lines: list, index_of_min_el: int):
    """
    Function increments the pointer of file from where line was taken.
    If pointer refers to end of file function will delete element from both lists:
        list of pointers and lines list

    :param pointer_list: list of pointers to files
    :param lines: list of lines of files that pointers are refer
    :param index_of_min_el: index of element in lines list that was writen to file
    """

    line = pointer_list[index_of_min_el].readline()
    if line == '' or line == '\n':
        pointer_list.pop(index_of_min_el)
        lines.pop(index_of_min_el)
    else:
        lines[index_of_min_el] = line


if __name__ == '__main__':
    start_time = time.time()
    tracemalloc.start()

    list_of_arguments = sys.argv

    try:
        path_to_logs_directory = list_of_arguments[1]
    except IndexError as err:
        path_to_logs_directory = '../logs'

    pointer_of_files = list()
    for file_ in get_list_of_files(path_to_logs_directory):
        pointer_of_files.append(open(join(path_to_logs_directory, file_), 'r'))

    combined_logs = open('combined_logs.log', 'w')

    values = list()
    for pointer in pointer_of_files:
        values.append(pointer.readline())

    while pointer_of_files:
        min_timestamp, index_of_min = get_min_of_timestamps(values)
        combined_logs.write(min_timestamp)
        get_next_line_of_file(pointer_of_files, values, index_of_min)

    combined_logs.close()

    end_time = time.time()

    current, peak = tracemalloc.get_traced_memory()
    print(f"Current memory usage is {current / 10 ** 6}MB; Peak was {peak / 10 ** 6}MB")
    print("Duration of script: ", str(end_time - start_time))
    tracemalloc.stop()
