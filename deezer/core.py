# -*- coding: utf-8 -*-
import re

file_regex = re.compile(r'^listen-[0-9]{8}.log$')
line_regex = re.compile(r'^[0-9]+[|][0-9]+[|][A-Z]{2}[|][0-9]+[|][0-9]+$')

def check_file(file):
    """Check if the file name is matching what we expect."""
    return file_regex.match(file)

def check_line(line):
    """Check if a line inside the logs file is as the expected format."""
    return line_regex.match(line)