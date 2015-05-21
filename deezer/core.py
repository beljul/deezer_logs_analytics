# -*- coding: utf-8 -*-
import re

file_regex = re.compile(r'^listen-[0-9]{8}.log$')

def check_file(file):
    """Check if the file name is matching what we expect."""
    return file_regex.match(file)