#!/usr/bin/env python
import re
from exceptions import *
from parser import Parser
from utils import mixl_open

if __name__ == '__main__':
    mixl_parser = Parser(mixl_open("test_script.mxl", ['./']), context={'red':'#FF0000'})
    mixl_parser.output()
