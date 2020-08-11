import xml.etree.ElementTree as ET
import sys
import urllib
import json
import argparse
import urllib.request
import glob
import requests

files = glob.glob("data/xmls_layered/*.xml")

for file in files:

	print(file)

	id = file.split("/")[-1].split(".")[0]

	prefix = ".//{http://www.tei-c.org/ns/1.0}"
	tree = ET.parse(file)
	ET.register_namespace('', "http://www.tei-c.org/ns/1.0")
	root = tree.getroot()

	arr = []

	items = root.findall("item")
	for item in items:
		if item.get("view") == "P":
			items2 = item.findall("item")

			prefix = "https://utda.github.io/kaishi/iiif/"+id

			canvas = prefix + "/canvas/p1"

			count = 0

			prefix_anno = prefix + "/annotation/p"

			for item2 in items2:
				if item2.get("name") != "blanc":

					info = "https://iiif.dl.itc.u-tokyo.ac.jp/iiif/kaishi/images/"+item2.get("name")+".tif/info.json"

					# 実際にAPIにリクエストを送信して結果を取得する
					r = requests.get(info)
					# 結果はJSON形式なのでデコードする
					data = json.loads(r.text)

					count += 1 

					obj = {
								"@id": prefix_anno+str(count).zfill(4)+"-image",
								"@type": "oa:Annotation",
								"motivation": "sc:painting",
								"resource": {
									"@id": "https://iiif.dl.itc.u-tokyo.ac.jp/iiif/kaishi/images/"+item2.get("name")+".tif/full/full/0/default.jpg",
									"@type": "dctypes:Image",
									"format": "image/jpeg",
									"width": data["width"],
									"height": data["height"],
									"service": {
										"@context": "http://iiif.io/api/image/2/context.json",
										"@id": "https://iiif.dl.itc.u-tokyo.ac.jp/iiif/kaishi/images/"+item2.get("name")+".tif",
										"profile": "http://iiif.io/api/image/2/level2.json"
									}
								},
								"on": canvas+"#xywh="+item2.get("locate")
							}
					arr.append(obj)

	fw = open(file.replace("xml", "json"), 'w')

	json.dump(arr, fw, ensure_ascii=False, indent=4,
			sort_keys=True, separators=(',', ': '))
