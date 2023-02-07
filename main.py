import requests
from bs4 import BeautifulSoup
import re
import json
from fastapi import FastAPI

app=FastAPI()


headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"}


@app.get("/getAllPlaces")
def getAllPlaces():
	places={
		"cities":set(),
		"states":set(),
		"countries":set()
	}
	link="https://bullions.co.in/location/india/"
	res=requests.get(link,headers=headers)
	soup=BeautifulSoup(res.text,"lxml")

	cities=soup.findAll("ul",{"class":"mega-sub-menu"})[0]
	for i in cities.findAll("a",{"class":"mega-menu-link"}):
		places["cities"].add(i.text.lower().replace(" ","-"))

	cities=soup.findAll("ul",{"class":"mega-sub-menu"})[1]
	for i in cities.findAll("a",{"class":"mega-menu-link"}):
		places["states"].add(i.text.lower().replace(" ","-"))

	cities=soup.findAll("ul",{"class":"mega-sub-menu"})[2]
	for i in cities.findAll("a",{"class":"mega-menu-link"}):
		places["countries"].add(i.text.lower().replace(" ","-"))

	return places


@app.get("/getGoldRate")
def getGoldRates(place="india"):
	link="https://bullions.co.in/location/"+place+"/"
	res=requests.get(link,headers=headers)
	soup=BeautifulSoup(res.text,"lxml")

	rates={"location":place.upper().replace("-"," "),"variations per 10g":{}}

	temp=soup.findAll("div",{"class":"data-box-half"})[0].findAll("div")
	rates[temp[0].text]={}
	rates[temp[0].text]["price"]=temp[1].text.strip()
	rates[temp[0].text]["change"]=temp[2].text
	rates[temp[0].text]["per value"]=temp[3].text


	for i in soup.findAll("table",{"class":"data"})[0].findAll("tr")[1:]:
		j=i.findAll("td")
		rates["variations per kg"][j[0].text]=j[2].text

	return rates
	

@app.get("/getSilverRate")
def getSilverRates(place="india"):
	link="https://bullions.co.in/location/"+place+"/"
	res=requests.get(link,headers=headers)
	soup=BeautifulSoup(res.text,"lxml")

	rates={"location":place.upper().replace("-"," "),"variations per 10g":{}}

	temp=soup.findAll("div",{"class":"data-box-half"})[1].findAll("div")
	rates[temp[0].text]={}
	rates[temp[0].text]["price"]=temp[1].text.strip()
	rates[temp[0].text]["change"]=temp[2].text
	rates[temp[0].text]["per value"]=temp[3].text


	for i in soup.findAll("table",{"class":"data"})[1].findAll("tr")[1:]:
		j=i.findAll("td")
		rates["variations per 10g"][j[0].text]=j[4].text

	return rates


@app.get("/getGoldPriceHistory")
def getGoldPriceHistory(place="india",no_of_days=30):
	link="https://bullions.co.in/location/"+place+"/"
	res=requests.get(link,headers=headers)

	raw_data="["+res.text.split("var chartData1=[")[1].split(",];")[0]+"]"
	raw_data=raw_data.replace("'",'"').replace("date",'"date"').replace("value",'"value"')
	data=json.loads(raw_data)

	return data[-1*int(no_of_days):]

@app.get("/getSilverPriceHistory")
def getSilverPriceHistory(place="india",no_of_days=30):
	link="https://bullions.co.in/location/"+place+"/"
	res=requests.get(link,headers=headers)

	raw_data="["+res.text.split("var chartData2=[")[1].split(",];")[0]+"]"
	raw_data=raw_data.replace("'",'"').replace("date",'"date"').replace("value",'"value"')
	data=json.loads(raw_data)

	return data[-1*int(no_of_days):]


#print(getSilverPriceHistory("hyderabad",30))
#getGoldPriceHistory("hyderabad",30)
#print(getSilverRates("vijayawada"))