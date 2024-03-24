import cv2 as cv
import mediapipe as mp
import keyboard as kb
# import json
# from . import parsing

error_margin = 0.1

def check_pose(pose):
	global error_margin
	pass

def record_pose(frame, results):
	countdown = 150
	if (countdown > 0):
		cv.putText(frame, text="3", org=(100,100), fontFace=cv.FONT_HERSHEY_TRIPLEX, fontScale=2, color=(100,100,100), thickness=3)
		countdown -= 1
	new_pose = results.multi_hand_landmarks

def capturing(mp_drawing, mp_hands):
	capture = cv.VideoCapture(0)
	if not capture.isOpened():
		print("Cannot open camera")
		exit()
	with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
		while True:
			ret, frame = capture.read()
			if not ret:
				print("Couldn't read frame. Exiting ...")
				break
			frame.flags.writeable = False
			# image = cv.cvtColor(image, cv.COLOR_BGR2RGB) #idk why it is used
			results = hands.process(frame)
			frame.flags.writeable = True
			# image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
			if (results.hand_landmarks):
				mp_drawing.draw_landmarks(frame, results.hand_landmarks, mp_hands.HAND_CONNECTIONS)
				check_pose(results)
			cv.imshow('Squat King', frame)
			if cv.waitKey(1) == ord('r'):
				record_pose(frame, results)
			if cv.waitKey(1) == ord('q'):
				break
	capture.release()
	cv.destroyAllWindows()

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
# saved_poses = load_poses("poses.pose")
capturing(mp_drawing, mp_hands)

# 1. json :)
# 2. please please please i know it's python but optimize it plsssssssss
# 3. points positions are relative not absolute (relative to nose maybe??)

#points: 1 nose, 2 eyes, 2 hands, 2 wrists, 2 elbows, 2 shoulders, 2 hips, 2 knees, 2 ankles = 17 points max