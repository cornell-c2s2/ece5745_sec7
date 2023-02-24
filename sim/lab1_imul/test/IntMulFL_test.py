#=========================================================================
# IntMulFL_test
#=========================================================================

import pytest

from random import randint

from pymtl3 import *
from pymtl3.stdlib.test_utils import mk_test_case_table, run_sim
from pymtl3.stdlib.stream import StreamSourceFL, StreamSinkFL

from lab1_imul.IntMulFL import IntMulFL

#-------------------------------------------------------------------------
# TestHarness
#-------------------------------------------------------------------------

class TestHarness( Component ):

  def construct( s, imul ):

    # Instantiate models

    s.src  = StreamSourceFL( Bits64 )
    s.sink = StreamSinkFL( Bits32 )
    s.imul = imul

    # Connect

    s.src.ostream  //= s.imul.istream
    s.imul.ostream //= s.sink.istream

  def done( s ):
    return s.src.done() and s.sink.done()

  def line_trace( s ):
    return s.src.line_trace() + " > " + s.imul.line_trace() + " > " + s.sink.line_trace()

#-------------------------------------------------------------------------
# mk_imsg/mk_omsg
#-------------------------------------------------------------------------

# Make input message, truncate ints to ensure they fit in 32 bits.

def mk_imsg( a, b ):
  return concat( Bits32( a, trunc_int=True ), Bits32( b, trunc_int=True ) )

# Make output message, truncate ints to ensure they fit in 32 bits.

def mk_omsg( a ):
  return Bits32( a, trunc_int=True )

#----------------------------------------------------------------------
# Test Case: small positive * positive
#----------------------------------------------------------------------

small_pos_pos_msgs = [
  mk_imsg(  2,  3 ), mk_omsg(   6 ),
  mk_imsg(  4,  5 ), mk_omsg(  20 ),
  mk_imsg(  3,  4 ), mk_omsg(  12 ),
  mk_imsg( 10, 13 ), mk_omsg( 130 ),
  mk_imsg(  8,  7 ), mk_omsg(  56 ),
]

# ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Define additional lists of input/output messages to create
# additional directed and random test cases.
# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''\/

#----------------------------------------------------------------------
# Test Case: small negative * positive
#----------------------------------------------------------------------

small_neg_pos_msgs = [
  mk_imsg(  -2,  3 ), mk_omsg(   -6 ),
  mk_imsg(  -4,  5 ), mk_omsg(  -20 ),
  mk_imsg(  -3,  4 ), mk_omsg(  -12 ),
  mk_imsg( -10, 13 ), mk_omsg( -130 ),
  mk_imsg(  -8,  7 ), mk_omsg(  -56 ),
]

#----------------------------------------------------------------------
# Test Case: small positive * negative
#----------------------------------------------------------------------

small_pos_neg_msgs = [
  mk_imsg(  2,  -3 ), mk_omsg(   -6 ),
  mk_imsg(  4,  -5 ), mk_omsg(  -20 ),
  mk_imsg(  3,  -4 ), mk_omsg(  -12 ),
  mk_imsg( 10, -13 ), mk_omsg( -130 ),
  mk_imsg(  8,  -7 ), mk_omsg(  -56 ),
]

#----------------------------------------------------------------------
# Test Case: small negative * negative
#----------------------------------------------------------------------

small_neg_neg_msgs = [
  mk_imsg(  -2,  -3 ), mk_omsg(   6 ),
  mk_imsg(  -4,  -5 ), mk_omsg(  20 ),
  mk_imsg(  -3,  -4 ), mk_omsg(  12 ),
  mk_imsg( -10, -13 ), mk_omsg( 130 ),
  mk_imsg(  -8,  -7 ), mk_omsg(  56 ),
]

#----------------------------------------------------------------------
# Test Case: large positive * positive
#----------------------------------------------------------------------

large_pos_pos_msgs = [
  mk_imsg( 0x0bcd0000, 0x0000abcd ), mk_omsg( 0x62290000 ),
  mk_imsg( 0x0fff0000, 0x0000ffff ), mk_omsg( 0xf0010000 ),
  mk_imsg( 0x0fff0000, 0x0fff0000 ), mk_omsg( 0x00000000 ),
  mk_imsg( 0x04e5f14d, 0x7839d4fc ), mk_omsg( 0x10524bcc ),
]

#----------------------------------------------------------------------
# Test Case: large negative * negative
#----------------------------------------------------------------------

large_neg_neg_msgs = [
  mk_imsg( 0x80000001, 0x80000001 ), mk_omsg( 0x00000001 ),
  mk_imsg( 0x8000abcd, 0x8000ef00 ), mk_omsg( 0x20646300 ),
  mk_imsg( 0x80340580, 0x8aadefc0 ), mk_omsg( 0x6fa6a000 ),
]

#----------------------------------------------------------------------
# Test Case: zeros
#----------------------------------------------------------------------

zeros_msgs = [
  mk_imsg(  0,  0 ), mk_omsg( 0 ),
  mk_imsg(  0,  1 ), mk_omsg( 0 ),
  mk_imsg(  1,  0 ), mk_omsg( 0 ),
  mk_imsg(  0, -1 ), mk_omsg( 0 ),
  mk_imsg( -1,  0 ), mk_omsg( 0 ),
]
#----------------------------------------------------------------------
# Test Case: random small
#----------------------------------------------------------------------

random_small_msgs = []
for i in range(50):
  a = randint(0,100)
  b = randint(0,100)
  random_small_msgs.extend([ mk_imsg( a, b ), mk_omsg( a * b ) ])

#----------------------------------------------------------------------
# Test Case: random large
#----------------------------------------------------------------------

random_large_msgs = []
for i in range(50):
  a = b32(randint(0,0xffffffff))
  b = b32(randint(0,0xffffffff))
  random_large_msgs.extend([ mk_imsg( a, b ), mk_omsg( a * b ) ])

#----------------------------------------------------------------------
# Test Case: lomask
#----------------------------------------------------------------------

random_lomask_msgs = []
for i in range(50):

  shift_amount = randint(0,16)
  a = randint(0,0xffffffff) << shift_amount

  shift_amount = randint(0,16)
  b = randint(0,0xffffffff) << shift_amount

  random_lomask_msgs.extend([ mk_imsg( a, b ), mk_omsg( a * b ) ])

#----------------------------------------------------------------------
# Test Case: himask
#----------------------------------------------------------------------

random_himask_msgs = []
for i in range(50):

  shift_amount = randint(0,16)
  a = randint(0,0xffffffff) >> shift_amount

  shift_amount = randint(0,16)
  b = randint(0,0xffffffff) >> shift_amount

  random_himask_msgs.extend([ mk_imsg( a, b ), mk_omsg( a * b ) ])

#----------------------------------------------------------------------
# Test Case: lohimask
#----------------------------------------------------------------------

random_lohimask_msgs = []
for i in range(50):

  rshift_amount = randint(0,12)
  lshift_amount = randint(0,12)
  a = (randint(0,0xffffff) >> rshift_amount) << lshift_amount

  rshift_amount = randint(0,12)
  lshift_amount = randint(0,12)
  b = (randint(0,0xffffff) >> rshift_amount) << lshift_amount

  random_lohimask_msgs.extend([ mk_imsg( a, b ), mk_omsg( a * b ) ])

#----------------------------------------------------------------------
# Test Case: sparse
#----------------------------------------------------------------------

random_sparse_msgs = []
for i in range(50):

  a = randint(0,0xffffffff)

  for i in range(32):
    is_masked = randint(0,1)
    if is_masked:
      a = a & ( (~(1 << i)) & 0xffffffff )

  b = randint(0,0xffffffff)

  for i in range(32):
    is_masked = randint(0,1)
    if is_masked:
      b = b & ( (~(1 << i)) & 0xffffffff )

  random_sparse_msgs.extend([ mk_imsg( a, b ), mk_omsg( a * b ) ])

# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''/\

#-------------------------------------------------------------------------
# Test Case Table
#-------------------------------------------------------------------------

test_case_table = mk_test_case_table([
  (                      "msgs                   src_delay sink_delay"),
  [ "small_pos_pos",     small_pos_pos_msgs,     0,        0          ],

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to leverage the additional lists
  # of request/response messages defined above, but also to test
  # different source/sink random delays.
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''\/

  [ "small_neg_pos",       small_neg_pos_msgs,    0,        0         ],
  [ "small_pos_neg",       small_pos_neg_msgs,    0,        0         ],
  [ "small_neg_neg",       small_neg_neg_msgs,    0,        0         ],
  [ "large_pos_pos",       large_pos_pos_msgs,    0,        0         ],
  [ "large_neg_neg",       large_neg_neg_msgs,    0,        0         ],
  [ "zeros",               zeros_msgs,            0,        0         ],
  [ "random_small",        random_small_msgs,     0,        0         ],
  [ "random_large",        random_large_msgs,     0,        0         ],
  [ "random_lomask",       random_lomask_msgs,    0,        0         ],
  [ "random_himask",       random_himask_msgs,    0,        0         ],
  [ "random_lohimask",     random_lohimask_msgs,  0,        0         ],
  [ "random_sparse",       random_sparse_msgs,    0,        0         ],
  [ "random_small_sink40", random_small_msgs,     0,       40         ],
  [ "random_small_src40",  random_small_msgs,    40,        0         ],
  [ "random_large_sink40", random_large_msgs,     0,       40         ],
  [ "random_large_src40",  random_large_msgs,    40,        0         ],

  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''/\

])

#-------------------------------------------------------------------------
# TestHarness
#-------------------------------------------------------------------------

@pytest.mark.parametrize( **test_case_table )
def test( test_params, cmdline_opts ):

  th = TestHarness( IntMulFL() )

  th.set_param("top.src.construct",
    msgs=test_params.msgs[::2],
    initial_delay=test_params.src_delay+3,
    interval_delay=test_params.src_delay )

  th.set_param("top.sink.construct",
    msgs=test_params.msgs[1::2],
    initial_delay=test_params.sink_delay+3,
    interval_delay=test_params.sink_delay )

  run_sim( th, cmdline_opts, duts=['imul'] )

