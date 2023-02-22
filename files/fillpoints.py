import math
from files import point
from files import path

def calcCurvature(p1, p2, p3):
  #find radius
  k1 = 0.5*( pow(p1.x,2) + pow(p1.y, 2) - pow(p2.x,2) - pow(p2.y,2)   ) /(p1.x - p2.x +0.0001)
  k2=(p1.y - p2.y)/(p1.x - p2.x)

  b= 0.5*( pow(p2.x,2) - 2*p2.x *k1 + pow(p2.y,2) - pow(p3.x,2) +2* p3.x *k1 - pow(p3.y,2))/(p3.x *k2 -p3.y +p2.y -p2.x *k2)
  a=k1 - k2 *b

  r = math.sqrt( pow((p1.x - a),2) +pow((p1.y - b),2) )

  #curvature = 1/radius
  curvature = 1/r

  return curvature


def FillPointVals(cpath, maxPathVelocity, kMaxVel, maxAcceleration):
  _path = cpath
  runningDistance = 0
  for i in range(len(_path.points)):
    #______Set the point distances from start of path______
    pointDistance = 0

    #if point is not the first
    if (i != 0):
      #find the difference between point i and point i-1
      pointDiff = point.getDistance(_path.getPoint(i-1), _path.getPoint(i)) 

      pointDistance = runningDistance + pointDiff
      runningDistance += pointDiff
    

    _path.points[i].setDistance(pointDistance)


    #______Set curvature of points______
    if (i != 0 and i != len(_path.points)-1):
      curvature = calcCurvature(_path.getPoint(i), _path.getPoint(i-1), _path.getPoint(i+1)) 

      _path.points[i].setCurvature(curvature) 
    else:
      _path.points[i].setCurvature(0.0000001)
    

    #______Set max velocity of points______
    #Set max velocity of point i to a minimum of (Max Path Velocity , k/curavture at point i)
    _path.points[i].setMaxVelocity(min(maxPathVelocity, kMaxVel/_path.getPoint(i).curvature))
  

  #----------Calculate Target Velocities-----------
  #1. simulate a robot running the path with max acceleration, starting at the end
  #2. vf = √(vi^2 + 2*a*d).
  # --> new velocity at point i = min(old target velocity at point i, √(velocity at point (i + 1))2 + 2 * a * distance )

  #Set velocity of last point to 0
  _path.points[len(_path.points)-1].setTargetVelocity(0)

  #loop through points back to front
  for i in range(len(_path.points)-2, -1, -1):
    pointDiff = _path.getPoint(i+1).distanceFromStart - _path.getPoint(i).distanceFromStart

    newTargetVelocity = min(_path.getPoint(i).maximumVelocity , math.sqrt(pow(_path.getPoint(i+1).targetVelocity,2) + (2*maxAcceleration*pointDiff)) )

    _path.points[i].setTargetVelocity(newTargetVelocity)
  

  return _path
