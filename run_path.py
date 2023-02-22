from files import pathsmoother, fillpoints




def SmoothPath(desPathArray, maxPathVelocity, kMaxVel,maxAcceleration ):
  desPath = pathsmoother.path.Path()
  for i in range(0,len(desPathArray),2):
    p = pathsmoother.point.Point(desPathArray[i], desPathArray[i+1])
    desPath.addPoint(p)
  desPath = pathsmoother.GenerateSmoothPath(desPath)
  return fillpoints.FillPointVals(desPath, maxPathVelocity, kMaxVel,maxAcceleration)  