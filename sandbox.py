#!/usr/bin/env python
import os

try:
    old_file = os.path.join("../../Desktop/", "output.txt")
except FileNotFoundError:
    old_file = open("../../Desktop/output.txt", mode='w+', encoding='utf-8')
    new_file = os.path.join("", "output.old")
    os.rename(old_file, new_file)
