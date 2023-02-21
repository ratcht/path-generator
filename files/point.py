import math

class Point :
  def setCoordinates(self, x, y):
    self.x = x
    self.y = y
  

  def setDistance(self, distanceFromStart):
    self.distanceFromStart = distanceFromStart
  

  def setCurvature(self, curvature) :
    self.curvature = curvature
  

  def setMaxVelocity(self, maximumVelocity) :
    self.maximumVelocity = maximumVelocity
  

  def setTargetVelocity(self, targetVelocity) :
    self.targetVelocity = targetVelocity
  

  def __init__ (self, x=None, y=None) :
    self.x = x
    self.y = y

  



#return the magnitude of a vector: c^2 = a^2 + b^2
def getMagnitude(point) :
  return math.sqrt(pow(point.x, 2) + pow(point.y, 2))



#calculates the distance between 2 points
def getDistance(p0, p1) :
  return getMagnitude(Point(p1.x - p0.x, p1.y - p0.y ))


