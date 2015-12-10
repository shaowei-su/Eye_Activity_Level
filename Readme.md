##Eye activity level (base on [eyeLike](https://github.com/trishume/eyeLike))

An eye activity level detector based on open source project _eyeLike_.

###SUMMARY
At this point of the semester I have researched and/or evaluated several third party eye tracking software packages for detecting pupil movement from video.  I have taken one of these packages (EyeLike) and implemented additional code to provide us with an eye-activity level feature.  Initial tests were completed and it appears this feature will be useful for deception detection.  For the rest of the semester I will be applying this feature to the deception data we are now gathering.

###PROBLEM STATEMENT

Design a video-extracted feature which characterizes eye movement level over a given duration of time for use in deception detection. More specifically, given the inputs:

INPUT:
A webcam-style video file recorded at ~15 FPS of an individual’s head
A list of video segments given in start/stop frame numbers

OUTPUT:
An eye activity level for each video segment

The difficulty in this problem comes from several factors, which my research will attempt to overcome:

* Low quality of the video files.
* resolution too low for straightforward pupil detection
* video image is noisy
* individuals may be of varying distance to webcam
* individuals may move their head during the video
* The need to obtain an activity level over a duration of time on the order of several seconds.


###BACKGROUND
A search of prior work identified a few tools developed for measuring pupil location from video.

* EyeLike - C++ package
-Timm and Barth. Accurate eye centre localisation by means of gradients. In Proceedings of the Int. Conference on Computer Theory and Applications (VISAPP), volume 1, pages 125-130, Algarve, Portugal, 2011. INSTICC.

* PyGaze - Python package
Dalmaijer, E.S., Mathôt, S., & Van der Stigchel, S. (2014). PyGaze: an open-source, cross-platform toolbox for minimal-effort programming of eye tracking experiments. Behavior Research Methods, 46, 913-921. doi:10.3758/s13428-013-0422-2

* The Eye Tribe - Hardware set + JAVA/C++ SDK
The Eye Tribe software enables eye control on mobile devices, allowing hands-­free navigation of websites and apps.

* xLabs - Chrome browser based gaze tracking system

Some of these projects depend on extra hardware supports and therefore are not used in my study. Also, none of these tools provide an “activity level over time”.  Most of the above efforts focus on gaze tracking: to use their eye gaze as an input that can be combined with other input devices like mouse, keyboard, touch and gestures.

Additionally, a generic energy calculation doesn’t fit in our experiments. On the one hand, a typical pupil tracking system begins with face detections and thus slight movement of head makes the results unstable and noisy. So input signal needs to be processed to eliminate noises before calculation. On the other hand, testers’ distance from camera may varies significantly from one record to another. Therefore results need to be normalized to a standard baseline for every sample. 


###METHODS

####Pupil Tracking
There are mainly two reasons why I picked EyeLike: 1. It supports low resolution videos; 2. It is accurate enough to detect trivial details. EyeLike uses image gradients and dot products to create a function that theoretically points out the center of the image’s most prominent circle, namely pupil. 

With the help of EyeLike, the position of left pupil (leftx, lefty) and right pupil (rightx, righty) can be tracked frame by frame and the output of this stage is a csv file that contains these values. 

####Signal Normalization
As discussed above, testers’ faces may appear at different positions around the image and EyeLIke normalizes out the face position but not the distance.To eliminate the influence of person’s distance from camera, I picked a standard eye distance value between left eye and right eye(S1). Then for tester with eye distance S2 and pupil movement distance(Δ2), the proportional movement in standard space should be Δ1 = Δ2 * S1 / S2.

####Noise Filtering
I used Butterworth low pass filter (built in Python scipy package) to cut out the variation in positions detected from a person sitting still without moving their eyes. With a first order, cutoff frequency 0.12 filter, the result can be seen from the image below.


####Activity calculation
After normalization and elimination of noises, eye activity is calculated by:
A = i = 1n|positioni - positioni - 1|n, 
where n is the number of frames; position composes of leftx, lefty, rightx and righty and needs to be computed separately.

####Testing
1. Pre-difined tests:

|  | Stable Eyes | Shifty Eyes |
| ------------ | ------------- | ------------ |
| Eye Activity Level | 1.87  | 4.04 |

2. Run with real datasets:

| Filename | Tell Truth | Eye Activity Level |
| ------------ | ------------- | ------------ |
| 2015-09-22_10-08-05-149-taylan | Yes  | 2.09 |
| 2015-09-21_22-48-13-207-qiyuan | No | 3.59 |


###FUTURE WORK THIS SEMESTER

For the remainder of the semester I plan to apply the EyeActivity feature to the video files obtained from the deception project.  I will do a statistical analysis to see if there are any differences between the eye activity level between individuals who are deceptive or not, as well as if there are differences in the level of activity based on the type of questions individuals answer.. 


###Building

CMake is required to build eyeLike.

###OSX or Linux with Make

```bash
# do things in the build directory so that we don't clog up the main directory
mkdir build
cd build
cmake ../
make
./bin/eyeLike # the executable file
```

###On OSX with XCode
```bash
mkdir build
./cmakeBuild.sh
```
then open the XCode project in the build folder and run from there.

###On Windows
There is some way to use CMake on Windows but I am not familiar with it.

###Blog Article:
Published by the _eyeLike_ author:

- [Using Fabian Timm's Algorithm](http://thume.ca/projects/2012/11/04/simple-accurate-eye-center-tracking-in-opencv/)

###Paper:
Timm and Barth. Accurate eye centre localisation by means of gradients.
In Proceedings of the Int. Conference on Computer Theory and
Applications (VISAPP), volume 1, pages 125-130, Algarve, Portugal,
2011. INSTICC.

(also see youtube video at http://www.youtube.com/watch?feature=player_embedded&v=aGmGyFLQAFM)

This document is a summary of my work this semester so far and my plans for the rest of the semester.



