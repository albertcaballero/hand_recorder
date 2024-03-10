import cv2 as cv
import mediapipe as mp
import keyboard as kb

error_margin = 0.1

def load_poses(fname):
	try:
		fd = open(fname, "r")
	except OSError:
		fd = open(fname, "x")
	fd.close()

def check_pose(pose):
	global error_margin
	pass

def record_pose(frame):
	countdown = 150
	if (countdown > 0):
		cv.putText(frame, text="3", org=(100,100), fontFace=cv.FONT_HERSHEY_TRIPLEX, fontScale=2, color=(100,100,100), thickness=3)
		countdown -= 1

def capturing(mp_drawing, mp_pose):
	capture = cv.VideoCapture(0)
	if not capture.isOpened():
		print("Cannot open camera")
		exit()
	with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
		while True:
			ret, frame = capture.read()
			if not ret:
				print("Can't receive frame (stream end?). Exiting ...")
				break
			# win_height, win_width, c = frame.shape
			results = pose.process(frame)
			mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
			if (results.pose_landmarks):
				check_pose(results)
			cv.imshow('Squat King', frame)
			if cv.waitKey(1) == ord('r'):
				record_pose(frame)
			if cv.waitKey(1) == ord('q'):
				break
	capture.release()
	cv.destroyAllWindows()

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
saved_poses = load_poses("poses.pose")
capturing(mp_drawing, mp_pose)

# 1. desing .pose file format
# 2. please please please i know it's python but optimize it plsssssssss