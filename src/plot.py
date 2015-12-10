#import plotly.plotly as py
#import plotly.graph_objs as go
import scipy.signal as signal
import numpy as np
import matplotlib.pyplot as plt

with open("afile--2015-09-21_22-48-13-207-qiyuan.txt") as f:
    content = f.readlines()
numFrames = len(content)
print numFrames
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

#remove lost video frames
leftXl = [leftX[0]]
leftYl = [leftY[0]]
rightXl = [rightX[0]]
rightYl = [rightY[0]]
eliminateRatio = 0.05
for i in range(1, numFrames - 1):
    curAvgLeft = (leftX[i] + leftX[i + 1]) / 2
    curAvgRight = (rightX[i] + rightX[i + 1]) / 2
    if curAvgLeft > (1 + eliminateRatio) * leftXl[-1] and curAvgRight < (1 - eliminateRatio) * rightXl[-1]:
        continue
    if curAvgLeft < (1 - eliminateRatio) * leftXl[-1] and curAvgRight > (1 + eliminateRatio) * rightXl[-1]:
        continue  
    leftXl.append(leftX[i])
    leftYl.append(leftY[i])
    rightXl.append(rightX[i])
    rightYl.append(rightY[i])

#update the number of frames
numFrames = len(leftXl)
framel = [i for i in range(numFrames)]
print numFrames
#normalize position movement parameter
#assume (rightX1 - leftX1) standard value as 130
#so delta(x1) = (rightX1 - leftX1) * deltax2 / (rightX2 - leftX1)
leftXn = [0 for i in range(numFrames)]
leftYn = [0 for i in range(numFrames)]
rightXn = [0 for i in range(numFrames)]
rightYn = [0 for i in range(numFrames)]
M = 130
for i in range(numFrames):
    leftXn[i] = M * leftXl[i] / (rightXl[i] - leftXl[i])
    leftYn[i] = M * leftYl[i] / (rightXl[i] - leftXl[i])
    rightXn[i] = M * rightXl[i] / (rightXl[i] - leftXl[i])
    rightYn[i] = M * rightYl[i] / (rightXl[i] - leftXl[i])


# First, design the Buterworth filter
N  = 1    # Filter order
low = 0.12 # Cutoff frequency
B, A = signal.butter(N, low, output='ba')
#high = .40 # Cutoff frequency # 1 = Nyquist frequency
#B, A = signal.butter(N, [low, high], btype='band')



# Second, apply the filter
leftXf = signal.filtfilt(B,A, leftXn)
leftYf = signal.filtfilt(B,A, leftYn)
rightXf = signal.filtfilt(B,A, rightXn)
rightYf = signal.filtfilt(B,A, rightYn)

#plot
plt.subplot(2, 2, 1)
plt.plot(frame, leftX, label='leftX')
plt.plot(frame, leftY, label='leftY')
plt.plot(frame, rightX, label='rightX')
plt.plot(frame, rightY, label='rightY')

plt.xlabel('frame #')
plt.ylabel('raw position val')
plt.title('filter results')
plt.legend(loc='upper left')
plt.grid(True)

plt.subplot(2, 2, 2)
plt.plot(framel, leftXl, label='leftXl')
plt.plot(framel, leftYl, label='leftYl')
plt.plot(framel, rightXl, label='rightXl')
plt.plot(framel, rightYl, label='rightYl')

plt.xlabel('frame #')
plt.ylabel('Eliminate lost frames position val')
plt.title('filter results')
plt.legend(loc='upper left')
plt.grid(True)

plt.subplot(2, 2, 3)
plt.plot(framel, leftXn, label='leftXn')
plt.plot(framel, leftYn, label='leftYn')
plt.plot(framel, rightXn, label='rightXn')
plt.plot(framel, rightYn, label='rightYn')

plt.xlabel('frame #')
plt.ylabel('UNfiltered-normalized position val')
plt.title('filter results')
plt.legend(loc='upper left')
plt.grid(True)


plt.subplot(2, 2, 4)
plt.plot(framel, leftXf, label='leftXf')
plt.plot(framel, leftYf, label='leftYf')
plt.plot(framel, rightXf, label='rightXf')
plt.plot(framel, rightYf, label='rightYf')

plt.xlabel('frame #')
plt.ylabel('filtered-normalized position val')
plt.title('filter results')
plt.legend(loc='upper right')
plt.grid(True)
plt.savefig("plot.png")



plt.show()

#average value
leftXAVG = sum(leftXf) / numFrames
leftYAVG = sum(leftYf) / numFrames
rightXAVG = sum(rightXf) / numFrames
rightYAVG = sum(rightYf) / numFrames

#compute the delta value
eyeActivity = 0
deltaLeftX = []
for i in range(1, len(leftXf)):
    deltaLeftX.append(abs(leftXf[i] - leftXf[i-1]))
eyeActivity += sum(deltaLeftX)
deltaLeftY = []
for i in range(1, len(leftYf)):
    deltaLeftY.append(abs(leftYf[i] - leftYf[i-1]))
eyeActivity += sum(deltaLeftY)
deltaRightX = []
for i in range(1, len(rightXf)):
    deltaRightX.append(abs(rightXf[i] - rightXf[i-1]))
eyeActivity += sum(deltaRightX)
deltaRightY = []
for i in range(1, len(rightYf)):
    deltaRightY.append(abs(rightYf[i] - rightYf[i-1]))
eyeActivity += sum(deltaRightY)

#activity per frame
apf = eyeActivity / numFrames
print("eyeActivity per frame = %f" % apf)
