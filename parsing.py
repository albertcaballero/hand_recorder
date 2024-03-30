import json
from mediapipe.framework.formats import landmark_pb2

class NormalizedLandmarkListEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, landmark_pb2.NormalizedLandmarkList):
			return {
				'id': 1,
				'landmarks': [
					{'x': landmark.x, 'y': landmark.y, 'z': landmark.z}
					for landmark in obj.landmark
				],
				'shortcut': ''
			}
		return json.JSONEncoder.default(self, obj)
	
class NormalizedLandmarkListDecoder(json.JSONDecoder):
	def decode(self, json_str):
		data = json.loads(json_str)
		if 'landmarks' in data:
			landmark_list = landmark_pb2.NormalizedLandmarkList()
			for landmark_data in data['landmarks']:
				landmark = landmark_list.landmark.add()
				landmark.x = landmark_data['x']
				landmark.y = landmark_data['y']
				landmark.z = landmark_data['z']
			return landmark_list
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

def check_file_content(poses):
	for i in poses:
		if len(poses[i]['points']) != 21:
			return False
		for j in poses[i]['points']:
			if len(poses[i]['points'][j]) != 3:
				return False
	return True

def load_poses(fname):
	file = check_file_permissions(fname)
	data = json.load(file, cls=NormalizedLandmarkListDecoder)
	# poses = data['poses']
	file.close()
	if check_file_content(poses) == False:
		exit
	return poses