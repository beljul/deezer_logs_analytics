# -*- coding: utf-8 -*-
import re
import os
from multiprocessing import Manager, Pool, cpu_count

file_regex = re.compile(r'^listen-[0-9]{8}.log$')
line_regex = re.compile(r'^[0-9]+[|][0-9]+[|][A-Z]{2}[|][0-9]+[|][0-9]+$')
markets = Manager().dict()

def check_file(file):
    """Check if the file name is matching what we expect."""
    return file_regex.match(file)

def check_line(line):
    """Check if a line inside the logs file is as the expected format."""
    return line_regex.match(line)

def parse_line(line):
    if not check_line(line): return
    data = line.split('|')
    if (data[0],data[2],data[1]) in markets:
        markets[(data[0],data[2],data[1])] += 1
    else:
        markets[(data[0],data[2],data[1])] = 1

def parse_file(file):
    """Parse a logs file from Deezer and get informations we need."""
    pool = Pool(processes=cpu_count())
    with open(file) as source_file:
        print source_file
        pool.map(parse_line, source_file, 3)
        pool.close()
        pool.join()
    print markets
    
def parse(dir):
    """
    Parse a directory which contains all the logs files provided by Deezer.
    Create a report for each provider in order to have informations about
    users who listen their songs (including market share).
    """
    for file in os.listdir(dir):
        if not check_file(file): continue
        parse_file(dir + '/' + file)