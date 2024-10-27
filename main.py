import cv2 as cv
import mediapipe as mp
import keyboard as kb
import json as js
import parsing

error_margin = 0.07

def exec_shortcut(loaded, idx):
	#add protections for invalid shortcuts and shit and idx out of range, try catch and that stuff
	if loaded[idx].shortcut == '[type shortcut here]':
		return
	print (loaded[idx].shortcut)
	if len(loaded[idx].shortcut) > 1 and '+' not in loaded[idx].shortcut:
		kb.write(loaded[idx].shortcut)
	else:
		kb.press_and_release(loaded[idx].shortcut)

def substract_landmark(landm1, landm2):
	if abs(landm1.x - landm2.x) > error_margin:
		return False
	if abs(landm1.y - landm2.y) > error_margin:
		return False
	if abs(landm1.z - landm2.z) > error_margin:
		return False
	return True

def compare_poses(loaded, pose):
	for i in range(21):
		if substract_landmark(pose.landmark[i], loaded.landmarklist.landmark[i]) == False:
			return False
	return True

def check_poses(pose, loadedPoses):
	global error_margin
	if len(loadedPoses) == 0:
		return -1
	normalize_pose(pose)
	for loaded in loadedPoses:
		if compare_poses(loaded, pose) == True:
			return loaded.idNum
	return -1

def normalize_pose(pose):
	base = [pose.landmark[0].x, pose.landmark[0].y, pose.landmark[0].z]
	i = 0
	#get distance from land[0] to land[5] to determine the (distance from camera/size of hand) and make it relative
	for i in range(21):
		pose.landmark[i].x -= base[0]
		pose.landmark[i].y -= base[1]
		pose.landmark[i].z -= base[2]

def record_pose(results, loaded):
	if (results.multi_hand_landmarks):
		new_pose = results.multi_hand_landmarks[0]
		normalize_pose(new_pose)
		kbshortcut = '[type shortcut here]'
		idx = len(loaded)
		app = parsing.loadedPose(landmarks=new_pose, shortcut=kbshortcut, idNum=idx)
		loaded.append(app)
	else:
		print("no pose detected")
		return 0

def capturing(mp_drawing, mp_hands, loaded_poses):
	capture = cv.VideoCapture(0)
	recCooldown = 0
	execCooldown = 0
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
				idx = check_poses(results.multi_hand_landmarks[0], loaded_poses)
				if idx >= 0 and execCooldown <= 0 and recCooldown <= 0:
					exec_shortcut(loaded_poses, idx)
					execCooldown = 40
			if kb.is_pressed('r+e+c') and recCooldown <= 0 and execCooldown <= 0:
				recCooldown = 40
				record_pose(results, loaded_poses)
			if recCooldown > 0:
				cv.putText(frame, text="Pls wait...", org=(100,100), fontFace=cv.FONT_HERSHEY_TRIPLEX, fontScale=2, color=(100,100,100), thickness=3)
				recCooldown -= 1
			if execCooldown > 0:
				cv.putText(frame, text="Executing...", org=(100,100), fontFace=cv.FONT_HERSHEY_TRIPLEX, fontScale=2, color=(100,100,100), thickness=3)
				execCooldown -= 1
			if cv.waitKey(1) == ord('q'):
				break
			cv.imshow('Pose recorder', frame)
	capture.release()
	cv.destroyAllWindows()

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
loaded_poses = parsing.load_poses("poses.pose")
capturing(mp_drawing, mp_hands, loaded_poses)
parsing.save_poses(loaded_poses)

#add way to delete poses
#add security copy to poses file
#split code in more files
#add way to add shortcut on recording