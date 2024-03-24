import json

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
	data = json.load(file)
	poses = data['poses']
	file.close()
	if check_file_content(poses) == False:
		exit
	return poses