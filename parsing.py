import json
from mediapipe.framework.formats import landmark_pb2

class loadedPose:
	def __init__(self, landmarks, idNum=1, shortcut = '') -> None:
		self.idNum = idNum
		self.landmarklist = landmarks
		self.shortcut = shortcut
	def __str__(self) -> str:
		return f"id={self.idNum},\nshortcut={self.shortcut},\nlandmarks={self.landmarks}"

class NormalizedLandmarkListEncoder(json.JSONEncoder):
	def default(self, loaded):
		if isinstance(loaded, loadedPose):
			landmark_lists_data = []
			for pose in loaded:
				landmark_list_data = {'landmarks': [], 'shortcut': '', 'id': 1}
				for landmark in loaded.landmark:
					landmark_list_data['landmarks'].append({'x': landmark.x, 'y': landmark.y, 'z': landmark.z})
				landmark_list_data['shortcut'] = "holii"
				landmark_list_data['id'] = 1
				landmark_lists_data.append(landmark_list_data)
			return {'landmark_lists': landmark_lists_data}
		return json.JSONEncoder.default(self, loadedPose)
	
class NormalizedLandmarkListDecoder(json.JSONDecoder):
	def decode(self, json_str):
		data = json.loads(json_str)
		if 'landmark_lists' in data:
			loadedArr = []
			for landmark_list_data in data['landmark_lists']:
				loaded = loadedPose(landmark_pb2.NormalizedLandmarkList())
				for landmark_data in landmark_list_data['landmarks']:
					point = loaded.landmarklist.landmark.add()
					point.x = landmark_data['x']
					point.y = landmark_data['y']
					point.z = landmark_data['z']
				loaded.idNum = landmark_list_data['id']
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
	file = open("./copy.json", "r")
	poses = json.load(file, cls=NormalizedLandmarkListDecoder)
	# poses = data['poses']
	file.close()
	return poses

def save_poses(loaded_poses):
	pose_file = open("./copy.json", "w")
	#needs to take into account all the previous poses
	json.dump(loaded_poses, pose_file, cls=NormalizedLandmarkListEncoder, indent=4)
	pose_file.close()