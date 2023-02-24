#=========================================================================
# Counter_test
#=========================================================================

import pytest

from pymtl3 import *
from pymtl3.stdlib.test_utils import run_test_vector_sim

from counter.CounterRTL import Counter


#=======================================================
# test_simple
#=======================================================
# Tests that our counter can count when enabled

def test_simple( cmdline_opts):
  run_test_vector_sim( Counter(),[
    ('en        out*'),
    [  1, 0x00000000 ],
    [  1, 0x00000001 ],
    [  1, 0x00000002 ],
  ],cmdline_opts)

#=======================================================
# test_enabled
#=======================================================
# Tests that our counter only counts when enabled

def test_enabled( cmdline_opts):
  run_test_vector_sim( Counter(),[
    ('en        out*'),
    [  1, 0x00000000 ],
    [  1, 0x00000001 ],
    [  0, 0x00000002 ],
    [  0, 0x00000002 ],
    [  0, 0x00000002 ],
    [  1, 0x00000002 ],
    [  1, 0x00000003 ],
    [  1, 0x00000004 ],
  ],cmdline_opts)