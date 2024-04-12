import json
from mediapipe.framework.formats import landmark_pb2

class loadedPose:
	def __init__(self, landmarks, idNum=1, shortcut = '') -> None:
		self.idNum = idNum
		self.landmarklist = landmarks
		self.shortcut = shortcut
	def __str__(self) -> str:
		return f"id={self.idNum},\nshortcut={self.shortcut},\nlandmarks={self.landmarks}"

def poseEncoder(loaded):
	if isinstance(loaded, list) and isinstance(loaded[0], loadedPose):
		data = []
		for pose in loaded:
			landmark_list_data = {'id': 1, 'shortcut': '', 'landmarks': []}
			for landmark in pose.landmarklist.landmark:
				landmark_list_data['landmarks'].append({'x': landmark.x, 'y': landmark.y, 'z': landmark.z})
			landmark_list_data['shortcut'] = pose.shortcut
			landmark_list_data['id'] = pose.idNum
			data.append(landmark_list_data)
		return {'landmark_lists': data}
	
class NormalizedLandmarkListDecoder(json.JSONDecoder):
	def decode(self, json_str):
		data = json.loads(json_str)
		if 'landmark_lists' in data:
			loadedArr = []
			i = 0
			for landmark_list_data in data['landmark_lists']:
				loaded = loadedPose(landmark_pb2.NormalizedLandmarkList())
				for landmark_data in landmark_list_data['landmarks']:
					point = loaded.landmarklist.landmark.add()
					point.x = landmark_data['x']
					point.y = landmark_data['y']
					point.z = landmark_data['z']
				loaded.idNum = i
				i += 1
				loaded.shortcut = landmark_list_data['shortcut']
				loadedArr.append(loaded)
			return loadedArr
		return json.JSONDecoder.decode(self, json_str)


def check_file_permissions(fname):
	try:
		file = open(fname, "r")
	except OSError:
		file = open(fname, "x")
	if not file.readable():
		print("File not readable, check permissions")
		file.close()
		exit
	if not file.writable():
		print("File not writable, check permissions")
		file.close()
		exit
	return file


def load_poses(fname):
	# file = check_file_permissions(fname)
	file = open("./pose.json", "r")
	poses = json.load(file, cls=NormalizedLandmarkListDecoder)
	file.close()
	return poses

def save_poses(loaded_poses):
	pose_file = open("./pose.json", "w")
	str = poseEncoder(loaded_poses)
	json.dump(str, pose_file, indent=4)
	pose_file.close()