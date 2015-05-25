# -*- coding: utf-8 -*-
from __future__ import division
import re
import os
from multiprocessing import Pool, cpu_count
import ntpath
import subprocess

file_regex = re.compile(r'^listen-[0-9]{8}.log$')
line_regex = re.compile(r'^[0-9]+[|][0-9]+[|][A-Z]{2}[|][0-9]+[|][0-9]+$')
id_regex = re.compile(r'[0-9]+')

markets = dict()
songs = dict()
users = dict()
market_share = dict()

def check_file(file):
    """Check if the file name is matching what we expect."""
    return file_regex.match(file)

def check_line(line):
    """Check if a line inside the logs file is as the expected format."""
    return line_regex.match(line)

def write_providers(content, file):
    """Write results from previous computing into file results. """
    # providers[0] = list of song_id,country,offer_id
    # providers[1] = nb_users
    # providers[2] = nb_listening
    # providers[3] = market_share
    dir = os.path.dirname(os.path.realpath(file))
    date = id_regex.findall(ntpath.basename(file))
    # Get the last iteration result
    providers = content[-1]
    # Write results
    for key in providers[0]:
        if not os.path.isdir(dir + "/results_" + date[0]):
            os.mkdir(dir + "/results_" + date[0])
        f = open(dir + "/results_" + date[0] + "/report_" + key + ".csv", "w")
        for tuple in providers[0][key]:
            song_id = tuple[0];
            country = tuple[1];
            offer_id = tuple[2];
            nb_stream = providers[2][(song_id, country, offer_id)];
            nb_users = len(providers[1][(song_id, country, offer_id)])
            nb_stream_total = providers[3][(country, offer_id)]
            f.write("{};{};{};{};{};{}\n".format(song_id, country, offer_id,
                                         nb_stream,
                                         nb_users,
                                         nb_stream / nb_stream_total))
        f.close()


def parse_line(line):
    """
    Parse a line in order to get all informations needed to compute what we need :
     - The listening number
     - The users number who listened
     - The market share (based on listening number)
    """
    if not check_line(line): return
    # data[0] = song_id
    # data[1] = user_id
    # data[2] = country
    # data[3] = provider_id
    # data[4] = offer_id
    data = line.split('|')
    # Remove \n
    data[4] = data[4].rstrip()
    
    # Get the listening number
    if (data[0], data[2], data[4]) in songs:
        songs[(data[0], data[2], data[4])] += 1
    else:
        songs[(data[0], data[2], data[4])] = 1
    
    # Get the users number
    if (data[0], data[2], data[4]) in users:
        users[(data[0], data[2], data[4])].add(data[1])
    else:
        users[(data[0], data[2], data[4])] = set()
        users[(data[0], data[2], data[4])].add(data[1])
        
    # Get the total listening number on a market
    if (data[2], data[4]) in market_share:
        market_share[(data[2], data[4])] += 1
    else:
        market_share[(data[2], data[4])] = 1
    
    # Get markets of the day
    if data[3] in markets:
        markets[data[3]].add((data[0], data[2], data[4]))
    else:
        markets[data[3]] = set()
        markets[data[3]].add((data[0], data[2], data[4]))
    return (markets, users, songs, market_share)

def parse_file(file):
    """Parse a logs file from Deezer and get informations we need."""
    pool = Pool(processes=cpu_count())
    with open(file) as source_file:
        wc_res = subprocess.check_output(['wc', '-l', file]).strip().split(' ')[0]
        # Let's processing
        res = pool.map(parse_line, source_file, int(int(wc_res)))
        pool.close()
        pool.join()
    write_providers(res, file)
    
def parse(dir):
    """
    Parse a directory which contains all the logs files provided by Deezer.
    Create a report for each provider in order to have informations about
    users who listen their songs (including market share).
    """
    for file in os.listdir(dir):
        if not check_file(file): continue
        parse_file(dir + '/' + file)