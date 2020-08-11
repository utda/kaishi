import xml.etree.ElementTree as ET
import sys
import urllib
import json
import argparse
import urllib.request
from rdflib import URIRef, BNode, Literal, Graph
import glob
import requests



prefix = ".//{http://www.tei-c.org/ns/1.0}"
tree = ET.parse("data/7-2-30.xml")
ET.register_namespace('', "http://www.tei-c.org/ns/1.0")
root = tree.getroot()

items = root.findall("item")
for item in items:
    if item.get("view") == "P":
        items2 = item.findall("item")
        for item2 in items2:
            if item2.get("name") != "blanc":
                obj = {
							"@id": "https://dzkimgs.l.u-tokyo.ac.jp/iiif/zuzoubu/01/ano1000",
							"@type": "oa:Annotation",
							"motivation": "sc:painting",
							"resource": {
								"@id": "https://iiif.dl.itc.u-tokyo.ac.jp/iiif/kaishi/images/"+item2.get("name")+".tif/full/full/0/default.jpg",
								"@type": "dctypes:Image",
								"format": "image/jpeg",
								"width": 5632,
								"height": 5976,
								"service": {
									"@context": "http://iiif.io/api/image/2/context.json",
									"@id": "https://iiif.dl.itc.u-tokyo.ac.jp/iiif/kaishi/images/"+item2.get("name")+".tif",
									"profile": "http://iiif.io/api/image/2/level1.json"
								}
							},
							"on": "https://dzkimgs.l.u-tokyo.ac.jp/iiif/zuzoubu/03/p0024#xywh="+item2.get("locate"),
							"license": "undefined",
							"attribution": "undefined"
						}
                print(",")
                print(obj)
