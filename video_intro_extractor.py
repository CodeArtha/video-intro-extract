from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import numpy as np
import cv2
from datetime import datetime

def video2frame(vidpath):
	# extract all the frames of the video and saves them to numbered .png images
	vidcap = cv2.VideoCapture(vidpath)
	success, image = vidcap.read()
	count = 0
	print(success)

	while success:
		cv2.imwrite("frame%d.png" % count, image)
		success, image = vidcap.read()
		# print("Read new frame: ", success)
		count += 1
	
	print("All frames saved as images")
	vidcap.release()
	cv2.destroyAllWindows()
	return count

def cutvideo(vid, startT, endT):
	# Extract a subclip from a video between t1 and t2. Time is in seconds.
	saveas = vid.split('.')[0] + "-cut." + vid.split('.')[1]
	ffmpeg_extract_subclip(vid, startT, endT, targetname=saveas)
	
	print("Shortened video saved as " + saveas)
	return 1

def mse(imageA, imageB):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])

	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err

def findframe(vid, pic):
	MSE_LIMIT = 50 # MSE under which we consider to have reached the best frame
	bestMSE = 1000000
	maxCount = 1000000
	bestCount = 0
	count = 0
	mse_limit_reached = False
	
	needle = cv2.imread(pic, cv2.IMREAD_UNCHANGED)
	
	vidcap = cv2.VideoCapture(vid)
	success, image = vidcap.read()

	while success:
		m = mse(needle, image)
		
		if m < bestMSE:
			bestMSE = m
			bestCount = count
			print("New best frame: {} with MSE of {}".format(count, bestMSE))
		
		# when we find a frame with an MSE belwo MSE_LIMIT, we let the script run 1000 frames further to see if there isn't any better and then stop.
		if (bestMSE < MSE_LIMIT) and (mse_limit_reached == False):
			maxCount = count + 1000
			mse_limit_reached = True
			
		if count >= maxCount:
			break
			
		success, image = vidcap.read()
		count += 1
	
	# cleanup and return
	print("Found the frame that match best")
	vidcap.release()
	cv2.destroyAllWindows()
	return [bestCount, bestMSE]

SRC_FPS = 29.97

selected_video = "video4.mkv"
frameNum, frameMSE = findframe(selected_video, "target_frame.png")
print(frameNum)

endtime = round(frameNum / SRC_FPS)
print(endtime)

cutvideo(selected_video, 0, endtime)


# lowest MSE video1.mp4 = 2.9 & 0.0
# video 2 is familly guy
# lowest MSE video3.mp4 = 9.9 & 5.6
# lowest MSE video4.mkv = 7.5 & 4.8

