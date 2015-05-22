# -*- coding: utf-8 -*-
import re
import os
from multiprocessing import Manager, Pool, cpu_count
import ntpath

file_regex = re.compile(r'^listen-[0-9]{8}.log$')
line_regex = re.compile(r'^[0-9]+[|][0-9]+[|][A-Z]{2}[|][0-9]+[|][0-9]+$')
id_regex = re.compile(r'[0-9]+')

markets = dict()
songs = Manager().dict()

def check_file(file):
    """Check if the file name is matching what we expect."""
    return file_regex.match(file)

def check_line(line):
    """Check if a line inside the logs file is as the expected format."""
    return line_regex.match(line)

def write_providers(content, file):
    dir = os.path.dirname(os.path.realpath(file))
    date = id_regex.findall(ntpath.basename(file))
    providers = content[-1]
    for key in providers:
        if not os.path.isdir(dir + "/results_" + date[0]):
            os.mkdir(dir + "/results_" + date[0])
        f = open(dir + "/results_" + date[0] + "/report_" + key + ".csv", "w")
        for tuple in providers[key]:
            song_id = tuple[0];
            country = tuple[1];
            offer_id = tuple[2];
            f.write("{};{};{};{}\n".format(song_id, country, offer_id,
                                         songs[(song_id, country, offer_id)]))
        f.close()

def parse_line(line):
    if not check_line(line): return
    # data[0] = song_id
    # data[1] = user_id
    # data[2] = country
    # data[3] = provider_id
    # data[4] = offer_id
    data = line.split('|')
    # Remove \n
    data[4] = data[4].rstrip()
    if (data[0], data[2], data[4]) in songs:
        songs[(data[0], data[2], data[4])] += 1
    else:
        songs[(data[0], data[2], data[4])] = 1
    if data[3] in markets:
        markets[data[3]].add((data[0], data[2], data[4]))
    else:
        markets[data[3]] = set()
        markets[data[3]].add((data[0], data[2], data[4]))
    return markets

def parse_file(file):
    """Parse a logs file from Deezer and get informations we need."""
    pool = Pool(processes=cpu_count())
    with open(file) as source_file:
        content = pool.map(parse_line, source_file, 3)
        pool.close()
        pool.join()
    write_providers(content, file)
    
def parse(dir):
    """
    Parse a directory which contains all the logs files provided by Deezer.
    Create a report for each provider in order to have informations about
    users who listen their songs (including market share).
    """
    for file in os.listdir(dir):
        if not check_file(file): continue
        parse_file(dir + '/' + file)