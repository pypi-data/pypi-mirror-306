from copy import deepcopy
import sys


ORIGINAL_SYS_ARGV = deepcopy(sys.argv)


def extend_to_sys_argv(string):
    sys.argv.extend(string.split())
    

def extend_to_original_sys_argv(string):
    sys.argv = deepcopy(ORIGINAL_SYS_ARGV)
    extend_to_sys_argv(string)
