#!/usr/bin/python
import plistlib
import re
import json
import os

def plist_to_json(f):
	dirname  = os.path.dirname(f)
	basename = os.path.basename(f).split('.')[0]
	json_data={
		"mc":{
			basename:{ "frameRate":10 }
		}
	}
	
	pl = plistlib.readPlist(f)

	res = {}
	frames=[]
	framePattern = re.compile(r'\{\{(\d+),(\d+)\},\{(\d+),(\d+)\}\}')
	offsetPattern = re.compile(r'\{-?(\d+),-?(\d+)\}')
	minX = 2048
	minY = 2048
	for key in sorted(pl["frames"].keys()):
		frame = pl["frames"][key]["frame"]
		offset = pl["frames"][key]["sourceColorRect"]
		mo = framePattern.match(frame)
		(x,y,w,h) = mo.groups()
		res[key] = {"x":int(x),"y":int(y),"w":int(w),"h":int(h)}

		mo = framePattern.match(offset)
		x = int(mo.group(1))
		y = int(mo.group(2))
		minX = min([x, minX])
		minY = min([y, minY])
		frames.append({"res" : key,"x" : x, "y" : y})

	for f in frames:
		f["x"] -= minX
		f["y"] -= minY
	json_data["mc"][basename]["frames"] = frames
	json_data["res"] = res

	with open(os.path.join(dirname, basename + ".json"), "w") as file:
		json.dump(json_data, file)

def plist_to_json_dir(d):
	for f in os.listdir(d):
		if not f.endswith('plist'):
			continue
		print('begin to process %s ...' % (f, ))
		plist_to_json(os.path.join(d, f))

if __name__ == '__main__':
	directories = [
		os.path.join('..', 'client', 'model'),
	]

	for d in directories:
		print('process directory %s ...' % (d, ))
		plist_to_json_dir(d)
