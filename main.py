import cv2 as cv
import mediapipe as mp
import keyboard as kb
# import json
# from . import parsing

error_margin = 0.1

def check_pose(pose):
	global error_margin
	return

def normalize_pose(pose):
	base = pose.landmark[0] #apparently this is not a deep copy and it's the same pointer, to do deep copy copy values manually xd
	print ("________base________\n", base)
	i = 0
	#get distance from land[0] to land[5] to determine the (distance from camera/size of hand) and make it relative
	while i < 21:
		print("before:", pose.landmark[i])
		pose.landmark[i].x -= base.x
		pose.landmark[i].y -= base.y
		pose.landmark[i].z -= base.z
		print("after:", pose.landmark[i])
		print ("base still:", base, "i is", i)
		i += 1
	print ("====================\n")

def record_pose(frame, results):
	countdown = 150
	if (countdown > 0):
		cv.putText(frame, text="3", org=(100,100), fontFace=cv.FONT_HERSHEY_TRIPLEX, fontScale=2, color=(100,100,100), thickness=3)
		countdown -= 1
	if (results.multi_hand_landmarks):
		new_pose = results.multi_hand_landmarks[0]
		normalize_pose(new_pose)
		return new_pose
	else:
		print("no pose detected")
		return False

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
			if (results.multi_hand_landmarks):
				for hand_landmarks in results.multi_hand_landmarks:
					mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
				check_pose(results)
			cv.imshow('Pose recorder', frame)
			if kb.is_pressed('r+e+c'):
				record_pose(frame, results)
			if cv.waitKey(1) == ord('q'):
				break
	capture.release()
	cv.destroyAllWindows()

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
# saved_poses = load_poses("poses.pose")
capturing(mp_drawing, mp_hands)
