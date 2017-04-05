#for windows and graphics
from tkinter import *

#function and variables to convert from polar to cartesian
from lineTools import Cart, _R1, _R2

from math import sin, cos

#dimmensions of the window
_width = 700
_height = 700

#takes a natural point and returns a real point (position on the screen in pixels)
def rp(natp):
	return [
		natp[0],
		-natp[1]+_height/2
	]

#takes a real point and returns a natural point, inverse of rp()
def np(realp):
	return [
		realp[0],
		-(realp[1]-_height/2)
	]

#opens a window for the user to draw in
#returns an array of lines
def getLines():
	#initialize window root
	root = Tk()

	#array to hold the lines
	lines = []

	def mousePressed(event):
		#makes window respond to keypresses
		frame.focus_set()

		#adds current click to new line
		lines.append([np([event.x, event.y])])

	def mouseReleased(event):
		#removes empty list if user did not move mouse while button was pressed
		if len(lines[-1]) < 2:
			lines.pop()

	def mouseMoved(event):
		#adds current mouse location
		lines[-1].append(np([event.x, event.y]))

		#draws the line
		start = rp(lines[-1][-2])
		end = rp(lines[-1][-1])
		frame.create_line(start[0], start[1], end[0], end[1])


	def keyPressed(event):
		#stops drawing when user presses enter
		if event.char == '\r':
			print("closing the window")
			root.destroy()

	#initialize window
	frame = Canvas(root, width=_width, height=_height)

	#bind functions to events
	frame.bind("<ButtonPress-1>", mousePressed)
	frame.bind("<ButtonRelease-1>", mouseReleased)
	frame.bind("<B1-Motion>", mouseMoved)
	frame.bind("<Key>", keyPressed)

	#display window
	frame.pack()
	frame.focus_set()

	#draw bounding ovals
	r1 = abs(_R1-_R2)
	r2 = abs(_R1+_R2)
	p1=rp([-r1, r1])
	p2=rp([r1,-r1])
	frame.create_oval(p1[0], p1[1], p2[0], p2[1])
	p1=rp([-r2,r2])
	p2=rp([r2,-r2])
	frame.create_oval(p1[0], p1[1], p2[0], p2[1])
	p1=rp([200, 100])
	p2=rp([500, -100])
	frame.create_rectangle(p1[0], p1[1], p2[0], p2[1])

	root.mainloop()
	return lines

#there may be an easier way to do this...
def sign(n):
	if n > 0:
		return 1
	return -1

#displays the polar points to check conversion
def dispPolar(lines, pol):

	#get root of window
	root = Tk()

	#end when user presses enter
	def keyPressed(event):
		if event.char == '\r':
			root.destroy()

	#decided to use can instead of frame this time
	can = Canvas(root, width=_width, height=_height)
	can.bind("<Key>", keyPressed)
	can.pack()

	#draw the origional lines
	for curve in lines:
		for i in range(len(curve)-1):
			start = rp(curve[i])
			end = rp(curve[i+1])
			can.create_line(start[0], start[1], end[0], end[1])
	
	#draw the polar path
	#plots lots of point to simulate non-linear movement at end of arm
	for curve in pol:
		for i in range(len(curve)-1):
			start = curve[i]
			end = curve[i+1]

			#limits arm movement
			minTheta = 0.01

			#overall change in theta
			dTheta = [
				end[0] - start[0],
				end[1] - start[1]
			]

			#dTheta limited by minTheta
			moveTheta = []

			#number of moveThetas in dTheta
			steps = 1

			if abs(dTheta[0]) < abs(dTheta[1]):
				#limit dTheta[1]
				moveTheta = [
					minTheta * abs(dTheta[0] / dTheta[1])*sign(dTheta[0]),
					minTheta * sign(dTheta[1])
				]
				steps = int(abs(dTheta[1]/minTheta))
			else:
				#limit dTheta[0]
				moveTheta = [
					minTheta * sign(dTheta[0]),
					minTheta * abs(dTheta[1] / dTheta[0]) * sign(dTheta[1])
				]
				steps = int(abs(dTheta[0]/minTheta))

			for j in range(steps):
				#pnt is the cartesian form of the polar angle
				pnt = rp(Cart([
					start[0] + moveTheta[0] * j,
					start[1] + moveTheta[1] * j
				]))
				#draw a small rectangle
				can.create_rectangle(pnt[0], pnt[1], pnt[0]+2, pnt[1]+2,
					fill='red',
					outline='red')

				armStart = rp([0,0])
				armMid = rp([
					_R1 * cos(start[0] + moveTheta[0] * j),
					_R1 * sin(start[0] + moveTheta[0] * j)
				])
				armEnd = rp([
					_R1 * cos(start[0] + moveTheta[0] * j) + _R2 * cos(start[1] + moveTheta[1] * j - (start[0] + moveTheta[0] * j)),
					_R1 * sin(start[0] + moveTheta[0] * j) + _R2 * sin(start[1] + moveTheta[1] * j - (start[0] + moveTheta[0] * j))
				])
				can.create_line(armStart[0], armStart[1], armMid[0], armMid[1])
				can.create_line(armMid[0], armMid[1], armEnd[0], armEnd[1])
				
			#draw the endpoint
			point = rp(Cart(end))
			can.create_rectangle(point[0], point[1], point[0]+2, point[1]+2,
				fill='red',
				outline='red')


	can.focus_set()
	root.mainloop()