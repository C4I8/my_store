import os
import json

paths=[os.path.join('..', 'assets', 'effect'), os.path.join('..', 'assets', 'model')]

def isTarget(f):
    return os.path.isfile(f) and f.endswith('json')

def doInDir(d, l):
    for f in os.listdir(d):
        path=os.path.join(d, f)
        if isTarget(path):
            l.append(path)
        elif os.path.isdir(path):
            doInDir(path, l)

def doJson(file):
	content = {}
	fileName = file[file.rindex(os.path.sep)+1:]
	fileName = fileName[:fileName.index(".json")]
	with open(file, "r") as f:
		content = json.load(f)
		tmp = content['mc']
		for (k,v) in tmp.items():
			tmp.pop(k)
			tmp[fileName] = v
			break

	with open(file, "w") as f:
		json.dump(content, f, sort_keys = True, indent = 4, separators = (',', ':'), ensure_ascii = False)


if __name__ == '__main__':
	results = []
	for p in paths:
		doInDir(p, results)
	for e in results:
		doJson(e)
