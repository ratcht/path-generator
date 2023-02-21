import math
from files import point, path, vector


def decimal_range(start, stop, increment):
    while start < stop: # and not math.isclose(start, stop): Py>3.5
        yield start
        start += increment

def CalcCoefficients(alpha, tension, p0, p1, p2, p3) :


  #Catmull-Rom Spline calculations
  t01 = pow(point.getDistance(p0, p1), alpha)
  t12 = pow(point.getDistance(p1, p2), alpha)
  t23 = pow(point.getDistance(p2, p3), alpha)

  m1 = []
  m2 = []

  #m1:
  #x:
  m1x = (1 - tension) * (p2.x - p1.x + t12 * ((p1.x - p0.x) / t01 - (p2.x - p0.x) / (t01 + t12)))
  #y:
  m1y = (1 - tension) * (p2.y - p1.y + t12 * ((p1.y - p0.y) / t01 - (p2.y - p0.y) / (t01 + t12)))

  m1.append(m1x)
  m1.append(m1y)


  #m2:
  #x:
  m2x = (1. - tension) * (p2.x - p1.x + t12 * ((p3.x - p2.x) / t23 - (p3.x - p1.x) / (t12 + t23)))

  #y:
  m2y = (1. - tension) * (p2.y - p1.y + t12 * ((p3.y - p2.y) / t23 - (p3.y - p1.y) / (t12 + t23)))

  m2.append(m2x)
  m2.append(m2y)

  segment = path.Segment()

  #Calculate segment coeffiecents using precalculated values
  segment.a = [ 2 * (p1.x - p2.x) + m1[0] + m2[0]  ,   2 * (p1.y - p2.y) + m1[1] + m2[1] ]
  segment.b = [ (-3) * (p1.x - p2.x) - m1[0] - m1[0] - m2[0]  ,  (-3) * (p1.y - p2.y) - m1[1] - m1[1] - m2[1] ]
  segment.c = [ m1[0] , m1[1] ]
  segment.d = [ p1.x, p1.y ]

  #point in spline = at^3 + bt^2 + ct + d
  #t is a point in the spline segment [0,1]

  return segment




def GenerateSmoothPath(desPath):

  #Inject a starting control point and ending control point
  #--> This is because splines need 2 control points to be generated
  #These control points are colinear with the 2 closest points

  #inject first control point

  firstPoint = desPath.getPoint(0)


  diff_x1 = desPath.getPoint(1).x - firstPoint.x
  diff_y1 = desPath.getPoint(1).y - firstPoint.y

  startingControl = point.Point( firstPoint.x - diff_x1, firstPoint.y - diff_y1 )

  desPath.points.insert(0,startingControl)


  #inject last control point
  lastPoint = desPath.getPoint(len(desPath.points) - 1)

  diff_x2 = lastPoint.x - desPath.getPoint(len(desPath.points) - 2).x
  diff_y2 = lastPoint.y - desPath.getPoint(len(desPath.points) - 2).y
  finalControl = point.Point( lastPoint.x + diff_x2, lastPoint.y + diff_y2 )

  desPath.points.append(finalControl)


  #Smooth Path
  segments = []
  for i in range(len(desPath.points) - 3):
    #Generate segment coefficients
    segment = CalcCoefficients(0.75, 0, desPath.getPoint(i), desPath.getPoint(i + 1), desPath.getPoint(i + 2), desPath.getPoint(i + 3))

    #add it to vector containing all segment coefficients
    segments.append(segment)
  


  smoothedPath = path.Path()

  #Loop through different segments
  for z in range(len(segments)):
    currentSegment = segments[z]

    #point in spline = at^3 + bt^2 + ct + d
    #t: [0,1], where 0 is the first point of the segment and 1 is the last
    #a, b, c, d were calculated above for each spline segment

    #add the first point of the first segment to the smoothedPath
    
    if (z == 0):
      xVal = segments[0].d[0]
      yVal = segments[0].d[1]
      smoothedPath.addPointVector([ xVal, yVal ])
    


    #generate an even number of points in each segment
    #t: [0, 1]
    #t increment: 0.1 => 10 points will be generated for each spine

    first = point.Point()
    first.x = currentSegment.d[0]
    first.y = currentSegment.d[1]

    last = point.Point()
    last.x = currentSegment.a[0] + currentSegment.b[0]  + currentSegment.c[0]  + currentSegment.d[0]
    last.y = (currentSegment.a[1]) + (currentSegment.b[1]) + (currentSegment.c[1] ) + currentSegment.d[1]

    distance = point.getDistance(first, last)

    #4 = distance between points
    numPoints = distance / 4
    increment = 1 / numPoints



    for t in decimal_range(increment,1+increment, increment):

      #point in spline = at^3 + bt^2 + ct + d
      xVal = (currentSegment.a[0] * pow(t, 3)) + (currentSegment.b[0] * pow(t, 2)) + (currentSegment.c[0] * t) + currentSegment.d[0]

      yVal = (currentSegment.a[1] * pow(t, 3)) + (currentSegment.b[1] * pow(t, 2)) + (currentSegment.c[1] * t) + currentSegment.d[1]

      xVal = round(xVal, 2)
      yVal = round(yVal, 2)
      #add generated point to smoothedPath
      smoothedPath.addPointVector([xVal, yVal ])
    

    smoothedPath.addPoint(last)


  

  return smoothedPath

