#=========================================================================
# IntMulVarCalcShamt PyMTL3 Wrapper
#=========================================================================

from pymtl3 import *
from pymtl3.passes.backends.verilog import *

class IntMulVarCalcShamt( VerilogPlaceholder, Component ):
  def construct( s ):
    s.in_ = InPort (8)
    s.out = OutPort(4)

