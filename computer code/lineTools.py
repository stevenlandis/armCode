from math import sqrt, acos, atan, pi, cos, sin
from sys import exit

#used to remove lines that are too close together
_minlength = 5

#number of iterations for binary search in allGood()
_iterations = 5

#number of tests in allGood()
_tests = 10

#length of the first arm segment (pixels)
_R1=6*50

#length of the second arm segment (pixels)
_R2=5.25*50

def dist(a, b):
	dx = b[0]-a[0]
	dy = b[1]-a[1]
	return sqrt(dx*dx + dy*dy)

#removes lines that are too close together
#treats parameter "lines" as call-by-reference
def clean(lines):
	N = 0
	for curve in lines:
		changed = True
		while changed:
			changed = False
			i = 0
			while i < len(curve)-2:
				start = curve[i]
				end = curve[i+1]
				if dist(start, end) < _minlength:
					curve.pop(i+1)
					N+=1
					i+=1
					changed = True

				i+=1
	print("Cleaned",N,"points")

#returns perpendicular distance between point and the line between start and end
def lineDist(point, start, end):
	P = [point[0]-start[0], point[1]-start[1]]
	D = [end[0]-start[1], end[1]-start[1]]
	base = sqrt(D[0]*D[0] + D[1]*D[1])
	area = abs(D[1]*P[0]-D[0]*P[1])
	#return the height
	return area/base

#law of cosines, returns angle given lengths of sides of triangle
def loc(a,b,c):
	return acos((a*a+b*b-c*c)/(2*a*b))

def arctan(x, y):
	#has the potential to deal with values form many quadrants
	return atan(y/x)

#returns polar version of a cartesian point
#inverse of Cart()
def Pol(point):
	R3=sqrt(point[0]*point[0] + point[1]*point[1])
	a1=arctan(point[0], point[1])
	a2=loc(_R1, R3, _R2)
	A=a1+a2
	#what happened to a3???
	a4=loc(_R1, _R2, R3)
	a5=pi-A
	B=a4-a5
	return [A,B - A]

#returns cartesian version of polar point
#inverse of Pol()
def Cart(angles):
	return [
		_R1 * cos(angles[0]) + _R2 * cos(angles[1] + angles[0]),
		_R1 * sin(angles[0]) + _R2 * sin(angles[1] + angles[0])
	]

#tests if polar version of line is straight enough
def allGood(start, end):
	Pstart = Pol(start)
	Pend = Pol(end)

	#linear movement between polar points
	dP = [
		(Pend[0] - Pstart[0]) / (_tests+1),
		(Pend[1] - Pstart[1]) / (_tests+1)
	]

	#moves between polar points
	for i in range(_tests):
		midPoint = [
			Pstart[0] + dP[0] * (i+1),
			Pstart[1] + dP[1] * (i+1)
		]
		#if the polar point is too far from the actual line, fail
		if lineDist(Cart(midPoint), start, end) > _minlength:
			return False
	return True

#returns the polar version of a list of lines
def polList(linelist):
	pol = []
	for curve in linelist:
		pol.append([Pol(curve[0])]);
		for i in range(len(curve)-1):
			start = curve[i]
			end = curve[i+1]

			reachedEnd = False

			while not(reachedEnd):
				if (allGood(start, end)):
					pol[-1].append(Pol(end))
					reachedEnd = True
				else:
					#list() copies the start array
					minp = list(start)
					maxp = list(end)

					#binary search for point where actual path strays from line too much
					for j in range(_iterations):
						mid = [
							(minp[0]+maxp[0])/2,
							(minp[1]+maxp[1])/2
						]
						if allGood(minp, mid):
							minp = mid
						else:
							maxp = mid
					start = mid
					pol[-1].append(Pol(mid))

	return pol

def stepList(pol):
	steps = []
	for curve in pol:
		steps.append([])
		for i in curve:
			steps[-1].append([
				(i[0]/(2*pi)*3*200)%600,
				(i[1]/(2*pi)*3*200)%600
			])
	return steps