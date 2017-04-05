This is a small python application for use with the sketchy arm.

It features a basic sketching program that:
	1. allows the user to draw a picture
	2. converts the lines into polar coordinates
	3. sends the polar coordinates to the Arduino powering the sketchy arm

Definitions used
	- Cartesian (Cart for short) refers to an (x, y) point
	- Polar (Pol for short) refers to a point (A1, A2)
		- A1 is the angle of the first pivot
		- A2 is the angle of the second pivot

To use this program:
	1. open main.py in terminal with the command "python3 main.py"
	2. draw your picture
	3. press enter to preview the path of the arm
	4. press enter to send the sketch to the arm