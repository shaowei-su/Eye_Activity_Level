import plotly.plotly as py
import plotly.graph_objs as go
import scipy.signal as signal
import numpy as np

with open("afile--tylan.txt") as f:
    content = f.readlines()
numFrames = len(content)
frame = [0 for i in range(numFrames)]
leftX = [0 for i in range(numFrames)]
leftY = [0 for i in range(numFrames)]
rightX = [0 for i in range(numFrames)]
rightY = [0 for i in range(numFrames)]

for i in range(numFrames):
	crtLine = content[i].split(",")
	frame[i] = crtLine[0]
	leftX[i] = crtLine[1]
	leftY[i] = crtLine[2]
	rightX[i] = crtLine[3]
	rightY[i] = crtLine[4]

#process list into numpy array
leftX = np.array(leftX)
leftX = leftX.astype(np.float)
leftY = np.array(leftY)
leftY = leftY.astype(np.float)
rightX = np.array(rightX)
rightX = rightX.astype(np.float)
rightY = np.array(rightY)
rightY = rightY.astype(np.float)

#normalize position movement parameter
#assume (rightX1 - leftX1) standard value as 130
#so delta(x1) = (rightX1 - leftX1) * deltax2 / (rightX2 - leftX1)
leftXn = [0 for i in range(numFrames)]
leftYn = [0 for i in range(numFrames)]
rightXn = [0 for i in range(numFrames)]
rightYn = [0 for i in range(numFrames)]
M = 130
for i in range(numFrames):
    leftXn[i] = M * leftX[i] / (rightX[i] - leftX[i])
    leftYn[i] = M * leftY[i] / (rightX[i] - leftX[i])
    rightXn[i] = M * rightX[i] / (rightX[i] - leftX[i])
    rightYn[i] = M * rightY[i] / (rightX[i] - leftX[i])



# First, design the Buterworth filter
N  = 1    # Filter order
low = 0.01
high = 0.03 # Cutoff frequency
B, A = signal.butter(N, [low, high], btype='band')

# Second, apply the filter
leftXf = signal.filtfilt(B,A, leftXn)
leftYf = signal.filtfilt(B,A, leftYn)
rightXf = signal.filtfilt(B,A, rightXn)
rightYf = signal.filtfilt(B,A, rightYn)
trace1 = go.Scatter(
    x=frame,
    y=leftXf,
    mode='lines+markers',
    name='left x'
)

trace2 = go.Scatter(
    x=frame,
    y=leftYf,
    mode='lines+markers',
    name='left y'
)

trace3 = go.Scatter(
    x=frame,
    y=rightXf,
    mode='lines+markers',
    name='right x'
)

trace4 = go.Scatter(
    x=frame,
    y=rightYf,
    mode='lines+markers',
    name='right y'
)
data = [trace1, trace2, trace3, trace4]
plot_url = py.plot(data, filename='line-scatter')


#compute the delta value
eyeActivity = 0
deltaLeftX = []
for i in range(len(leftXf)):
    deltaLeftX.append(abs(leftXf[i]))
eyeActivity += sum(deltaLeftX)
deltaLeftY = []
for i in range(len(leftYf)):
    deltaLeftY.append(abs(leftYf[i]))
eyeActivity += sum(deltaLeftY)
deltaRightX = []
for i in range(len(rightXf)):
    deltaRightX.append(abs(rightXf[i]))
eyeActivity += sum(deltaRightX)
deltaRightY = []
for i in range(len(rightYf)):
    deltaRightY.append(abs(rightYf[i]))
eyeActivity += sum(deltaRightY)

#activity per frame
apf = eyeActivity / numFrames
print"eyeActivity per frame = %f" % apf
