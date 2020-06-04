#!/usr/bin/python3

import sys
import urllib.request
import json
import requests
import shutil
import numpy as np
import matplotlib.pyplot as plt
import os.path, os

def main(immo_viewer_url):
	# get response of viewer url
	with urllib.request.urlopen(immo_viewer_url) as response:
		html = response.read()

		# extract config json (window.jsonData=) and parse
		json_config = str(html.decode('utf8')).split("window.jsonData=")[1].split('\n')[0][:-1]
		config = json.loads(json_config)

		# iterate over tour->rooms list
		for roomkey, roomsubdict in config["tour"]["rooms"].items():
			# find highest res version
			highestres_pattern = ""
			highrestres_value = 0
			for tilesubdict in roomsubdict["tilesDesktop"]["levels"]:
				if tilesubdict["tiledImageWidth"] > highrestres_value:
					highrestres_value = tilesubdict["tiledImageWidth"]
					highestres_pattern = tilesubdict["cubePattern"]

			# save cube images per room
			download_room(roomsubdict["name"], highestres_pattern, highrestres_value)

def download_room(name, url_pattern, cube_size):
	cube_sides = ['l', 'f', 'r', 'b', 'u', 'd'] # https://krpano.com/docu/panoformats/index.php?lang=de
	fname_base = name.replace("/", "-").strip() + "_{}_{}_{}.jpg"

	for s in cube_sides:
		# download all sides
		for v in range(1, 3):
			for h in range(1, 3):
				cur_fname = fname_base.format(s, str(v), str(h))
				url = url_pattern.replace("%s", s).replace("%v", str(v)).replace("%h", str(h)).replace("JPG", "jpg")
				print(name + ": " + url)

				r = requests.get(url, stream=True)
				if r.status_code == 200:
				    r.raw.decode_content = True
				    
				    with open(cur_fname,'wb') as f:
				    	shutil.copyfileobj(r.raw, f)				        
				else:
				    print('Image Couldn\'t be retreived: ' + url_pattern)

		# stitch
		full = np.zeros((cube_size, cube_size, 3))
		full.astype(int)

		t11 = plt.imread(fname_base.format(s, str(1), str(1)))
		t12 = plt.imread(fname_base.format(s, str(1), str(2)))
		t21 = plt.imread(fname_base.format(s, str(2), str(1)))
		t22 = plt.imread(fname_base.format(s, str(2), str(2)))

		full[0:t11.shape[0], 0:t11.shape[1]] = t11
		full[0:t12.shape[0], t11.shape[1]:(t11.shape[1] + t12.shape[1])] = t12
		full[t11.shape[0]:(t11.shape[0]+t21.shape[0]), 0:t21.shape[1]] = t21
		full[t12.shape[0]:(t12.shape[0]+t22.shape[0]), t21.shape[1]:(t21.shape[1] + t22.shape[1])] = t22

		os.remove(fname_base.format(s, str(1), str(1))) 
		os.remove(fname_base.format(s, str(1), str(2))) 
		os.remove(fname_base.format(s, str(2), str(1))) 
		os.remove(fname_base.format(s, str(2), str(2))) 

		plt.imsave(name.replace("/", "-").strip() + "_{}.jpg".format(s), full.astype(np.uint8))


main(sys.argv[1])