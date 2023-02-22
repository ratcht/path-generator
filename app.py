from flask import Flask, redirect, url_for, render_template, request
from run_path import SmoothPath
import json

app = Flask(__name__)
maxPathVelocity = 100#//inches per second
kMaxVel = 3 #1,5] higher k --> faster around turns 
lookaheadDistance = 40
maxAcceleration = 100 #incher per second^2


gPoints = []


@app.route("/submit",methods=["POST"])
def submit():
    global gPoints
    newPoints = []
    with open('text/genpath.txt', 'w') as f:
        if request.method == "POST":
            points = request.get_json()
            desPath = SmoothPath(points, maxPathVelocity, kMaxVel,maxAcceleration )
            
            for p in desPath.points:
                newPoints.append(p.x)
                newPoints.append(p.y)
                f.write(str(p.x))
                f.write(",")
                f.write(str(p.y))
                f.write(",")
                f.write(str(p.targetVelocity))
                f.write(",")
                f.write(str(p.distanceFromStart))
                f.write(",")
                f.write(str(p.curvature))
                f.write("\n")

            gPoints = newPoints

            

    return json.dumps(newPoints)

@app.route("/reset")
def reset():
    global gPoints
    gPoints = []
    return redirect(url_for('index'))

    
@app.route("/")
def index():
    global gPoints
    return render_template("index.html")

if __name__ == "__main__":
    app.run()