# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'

# %%
from bs4 import BeautifulSoup
import subprocess
import json
import requests


# %%
req = requests.get("https://www.herrenberg.de/de/Stadtleben/Erlebnis-Herrenberg/Service/Parkplaetze")
soup = BeautifulSoup(req.text)


# %%
parsedLinks = []

# Filter links that href=#
for a in soup.find(id="mainColArea").find_all('a'):
    if a['href'].find("#") == -1:
        link = a['href'].replace('&amp;', '&')
        parsedLinks.append(link)


# %%
dictlist = [dict() for x in range(0, 16)]
i = 0
exception = parsedLinks.pop(13)
for a in parsedLinks:
    req = requests.get(a)
    html = BeautifulSoup(req.text)
    dataDiv = html.find(id="mainContentArea")
    dictlist[i] = {
      "type": "Feature",
      "geometry": {
          "type": "Point",
          "coordinates": [
              str(dataDiv.find("a", {"target": "googleMaps"})['href']).split("=")[1].split("%2C")[1],
              str(dataDiv.find("a", {"target": "googleMaps"})['href']).split("=")[1].split("%2C")[0]
          ]
      },
      "properties": {
          "name": dataDiv.h2.text.split(",")[0],
          "address": str(dataDiv.find("div", {"class": "cCore_addressBlock_address"})).split("<br/>")[1],
          "capacity": int(dataDiv.h2.text.split(", ")[1].split(" ")[0]),
      }
    }
    i = i + 1


# %%
req = requests.get(exception)
html = BeautifulSoup(req.text)
dataDiv = html.find(id="mainContentArea")
dictlist[15] = {
  "type": "Feature",
  "geometry": {
      "type": "Point",
      "coordinates": [
          "8.86822",
          "48.59946"
      ]
  },
  "properties": {
      "name": dataDiv.h2.text.split(",")[0],
      "address": str(dataDiv.find("div", {"class": "cCore_addressBlock_address"})).split("<br/>")[1],
      "capacity": int(dataDiv.h2.text.split(" ")[1]),
  }
}


# %%
park = {
    "type": "FeatureCollection",
    "features": dictlist
}


# %%
with open('parking_lots.geojson', 'w') as fp:
    json.dump(park, fp)


