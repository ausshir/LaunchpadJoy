import rtmidi
from rtmidi.midiutil import open_midiport
import vjoy
import time

# Midi Stuff
midiout = rtmidi.MidiOut()
midiout.open_port(1)
midiin, port_name = open_midiport(1)

# Joystick Stuff
joyState = [vjoy.JoystickState(), vjoy.JoystickState()]
vjoy.Initialize()

# LED Addressing
# OFF,R,G,A,Y
color = [0x00, 0x0F, 0x3C, 0x3F, 0x3E]
# From top left to bottom right
pos = [[0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08],
		[0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18],
		[0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28],
		[0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38],
		[0x40, 0x41, 0x42, 0x43, 0x44, 0x45, 0x46, 0x47, 0x48],
		[0x50, 0x51, 0x52, 0x53, 0x54, 0x55, 0x56, 0x57, 0x58],
		[0x60, 0x61, 0x62, 0x63, 0x64, 0x65, 0x66, 0x67, 0x68],
		[0x70, 0x71, 0x72, 0x73, 0x74, 0x75, 0x76, 0x77, 0x78]]
		
# Button -> Joystick Addressing
assign = [None] * 121
assign[0] = 0
assign[1] = 1
assign[2] = 2
assign[3] = 3
assign[4] = 4
assign[5] = 5
assign[6] = 6
assign[7] = 7
assign[16] = 8
assign[17] = 9
assign[18] = 10
assign[19] = 11
assign[20] = 12
assign[21] = 13
assign[22] = 14
assign[23] = 15

pressed = [False] * 121

# Button -> Light translator
def b2l(keyNum):
	y = keyNum % 16
	x = int(keyNum / 16)
	
	return [x,y]


# Maintains Background Lighting
def lightState(buttons):
	i = 0
	while(i < 8):
		note = [0x90, pos[i][0], color[2]]
		midiout.send_message(note)
		i += 1


		
timer = time.time()

try:
	while(1):
	
		if((time.time() - timer) >= 200):
			timer = time.time()
			vjoy.Initialize()
			#print "reinit"
			
		#	
		#note = [0x90, pos[j][i], color[k]]
		#midiout.send_message(note)
		#if(i == 7):
		#	i = 0
		#	j += 1
		#else:
		#	i += 1
		#if(j == 8):
		#	j = 0
		#	k += 1
		#if(k == 4):
		#	k = 0
		#	
		#print (i,j,k)
		
		msg = midiin.get_message()
		if msg:
			message, delta = msg
			print message
			button = assign[message[1]]
			keyLight = b2l(message[1])
			
			if(message[2] == 127):
				print "set", button
				if button is not None:
					vjoy.SetButton(joyState[0], button, vjoy.BUTTON_DOWN)
				midiout.send_message([0x90, pos[keyLight[0]][keyLight[1]], color[1]])
				pressed[button] = True
			
			elif(message[2] == 0):
				print "unset", button
				if button is not None:
					vjoy.SetButton(joyState[0], button, vjoy.BUTTON_UP)
				midiout.send_message([0x90, pos[keyLight[0]][keyLight[1]], color[0]])
				pressed[button] = False
	
		vjoy.UpdateJoyState(1, joyState[0])
		
		lightState()
			
	
except:
	print "Closing Ports"
	midiout.close_port()
	midiin.close_port()
	vjoy.Shutdown()
	raise