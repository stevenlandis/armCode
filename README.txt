I worked in a group to make a robotic arm that can draw pictures using a pen.

This repository contains the code that runs on the Arduino and the code that runs on the computer.

Arduino Code
	You should be able to use the Arduino IDE to run the code.

Computer Code
	This requires a bit more setup.
	I only tested this on my computer (mac), so you may need to install some extra libraries to make this work.

	Also, you will need to use the Arduino IDE to find the usb port address.
		This is /dev/cu.usbmodem14121 on my computer, it will probably be different on yours
		Once you find the address, go to "sendingInstructions.py" and change the serialAddress variable at the top.

	To run the python app:
		1. navigate in your terminal to the directory named "computer code"
		2. execute the command "python3 main.py"
	
	When this runs, you should see a window pop up to draw pictures.
	Click and drag to draw the pictures.
	Once you are done, press ENTER to send the instructions and begin drawing.
