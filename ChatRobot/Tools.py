#coding=utf8
import re

def write_file(stream_data, file_dir, mode):
    with open(file_dir, mode) as f:
        f.write(stream_data)