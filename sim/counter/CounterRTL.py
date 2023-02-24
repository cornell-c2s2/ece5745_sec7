# This is the PyMTL wrapper for the corresponding Verilog RTL model RegIncVRTL.

from pymtl3 import *
from pymtl3.stdlib import stream
from pymtl3.passes.backends.verilog import *


class CounterVRTL( VerilogPlaceholder, Component ):

  # Constructor

  def construct( s ):
    # If translated into Verilog, we use the explicit name

    s.set_metadata( VerilogTranslationPass.explicit_module_name, 'Counter' )

    # Interface
    s.en  = InPort (  1 )
    s.out = OutPort( 32 )


Counter = CounterVRTL
