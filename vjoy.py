"""
Python bindings for Headsoft's VJoy driver version 1.2.
You can find VJoy here:  http://headsoft.com.au/index.php?category=vjoy
"""

from ctypes import *

__VERSION__ = 1.2
__AUTHOR__ = "Brent Taylor"
__CONTACT__ = "btaylor@fuzzylogicstudios.com"

POV_UP = 0
POV_RIGHT = 1
POV_DOWN = 2
POV_LEFT = 3
POV_NIL = 4

AXIS_MIN = -32767
AXIS_NIL = 0
AXIS_MAX = 32767

BUTTON_UP = 0
BUTTON_DOWN = 1

__vjoy = windll.VJoy

class JoystickState(Structure):
	"""
	Proposed Joystick State.

	A structure outlining the proposed state of the virtual joystick.
	All axis range from AXIS_MIN (default: -32767) to AXIS_MAX (default: 32767).

	"""
	_pack_ = 1
	_fields_ = [("ReportId", c_ubyte),
		("XAxis", c_short),
		("YAxis", c_short),
		("ZAxis", c_short),
		("XRotation", c_short),
		("YRotation", c_short),
		("ZRotation", c_short),
		("Slider", c_short),
		("Dial", c_short),
		("POV", c_ushort),
		("Buttons", c_uint32)]

def Initialize(name = "", serial = ""):
	return __vjoy.VJoy_Initialize(name, serial)

def Shutdown():
	return __vjoy.VJoy_Shutdown()

def UpdateJoyState(Index, JoyState):
	return __vjoy.VJoy_UpdateJoyState(Index, byref(JoyState))

def SetPOV(JoyState, Index, State):
	JoyState.POV &= ~(0xf << ((3 - Index) * 4))
	JoyState.POV |= State << ((3 - Index) * 4)

def SetButton(JoyState, Index, State):
	if State == BUTTON_DOWN:
		JoyState.Buttons |= 1 << Index
	else:
		JoyState.Buttons &= ~(1 << Index)

