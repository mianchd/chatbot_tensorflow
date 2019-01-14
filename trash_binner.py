"""


"""


import requests
from bs4 import BeautifulSoup

def extractBin(urlstring):
	if urlstring is not None:
		if "garbage" in urlstring:
			return "Garbage"
		elif "blue-box" in urlstring:
			return "Recyclable"
		elif "crc" in urlstring:
			return "Community Recycling Centre"
		elif "special" in urlstring:
			return "Agricultural Recyclable"
		else:
			return "Not Sure"


def getBin(queryStr = "Plastic+bags"):
    base_uri = 'http://www.peelregion.ca'
    sec_uri = "/scripts/waste/how-to-sort-your-waste.pl?action=search&query="
    query = queryStr

    res = requests.get(base_uri + sec_uri + query)

    if res.status_code == 200:
        print("RAW HTML obtained")
    else:
        print("Problem communicating to the Web Source")
        return 0

    soup = BeautifulSoup(res.content, "lxml")

    items_list = soup.findAll(name="div", attrs={"class": "wmWhereMultiItem"})

    if len(items_list) == 0:
        print("Got no results from the websource!")
        return "Got no results from the websource!"

    mylist = []
    for item in items_list[:10]:
    	templist = []
    	templist.append(item.find('a').contents[0].encode())
    	templist.append(extractBin(item.find('img')['src']))
    	mylist.append(templist)

    return mylist


if __name__ == '__main__':
    getBin()
