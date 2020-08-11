import xml.etree.ElementTree as ET
import sys
import urllib
import json
import argparse
import urllib.request
from rdflib import URIRef, BNode, Literal, Graph
import glob
import requests

files = glob.glob("xmls/*.xml")

prefix = ".//{http://www.tei-c.org/ns/1.0}"

ET.register_namespace('', "http://www.tei-c.org/ns/1.0")


rows = []
rows.append(["Item Identifier", "Media Url", "Title", "label"])

check = []
count = []

for file in sorted(files):
	tree = ET.parse(file)
	root = tree.getroot()

	id = file.split("/")[-1].split(".")[0]

	title = root.get("title")

	flg = False

	items = root.findall("item")
	for item in items:

		label = item.get("label")

		if item.get("resource"):

			if item.get("ext") == "jpg":
				flg = True
				api = ""

			if item.get("ext") == "fzp":
				res = item.get("resource")
				res = res.split("/")[-1]
				api = "https://iiif.dl.itc.u-tokyo.ac.jp/iiif/kaishi/images/" + res + ".tif/info.json"
				count.append(api)
		
		rows.append([id, api, title, label])

	if flg:
		check.append(file)

print(check)
print(len(check))

print(len(count))

import csv

with open('data/images.csv', 'w') as f:
    writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく
    writer.writerows(rows) # 2次元配列も書き込める

