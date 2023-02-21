import math
from files import point


class Path:
  #deque is used here instead of vector as it makes it easy to push points to the front
  #point --> a vector of [x,y]

  def __init__(self):
    self.points = []

  #returns a point
  def getPoint(self, t):
    return self.points[t]
  


  #adds a point
  def addPoint(self, p):
    self.points.append(p)
  

  def addPointVector(self, vPoint):
    p = point.Point(vPoint[0], vPoint[1])
    self.points.append(p)


class Segment:
  def __init__(self):
    self.a = []
    self.b = []
    self.c = []
    self.d = []


  


