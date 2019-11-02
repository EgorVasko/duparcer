#!/usr/bin/env python


test_dict = {"c":1}
#test_dict = {}

if test_dict:
    print("Dict is not Empty")

if not test_dict:
    print("Dict is Empty")


if not bool(test_dict):
    print("Dict is Empty")


if len(test_dict) == 0:
    print("Dict is Empty")
