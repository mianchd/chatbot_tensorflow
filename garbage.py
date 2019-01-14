import requests
from bs4 import BeautifulSoup
import json

def getDates(trash_type = None):

    address = None
    with open("address.db", "r") as db:
        dbString = db.read()
        dbJson = json.loads(dbString)
        address = dbJson['current']

    base_uri = 'http://www.peelregion.ca'
    vals = "/waste-scripts/when-does-it-go/default.asp?action=search&town=&query="

    res = requests.get(base_uri + vals + address)

    if res.status_code == 200:
        print("Response received from Source")
    else:
        print("Problem communicating to the Web Source for Garbage Schedule")
        return 0

    soup = BeautifulSoup(res.content, "lxml")

    addr_list = soup.findAll(name="div", attrs={"class": "wmWhenMultiItem"})

    if len(addr_list) > 0:
        return "Address not matched, let me know of your address by typing <b>addr: your_address</b> <br><br>" + '<br>'.join([addr.text for addr in addr_list]).replace('\\n', '<br>')

        """
        below is command line testing
        """
        addr_dict = {}
        for addr in addr_list:
            addr_dict[addr.text] = addr.find('a')['href']

        for addr, link in addr_dict.items():
            print(addr)
        #    print(link)
        addr_index = input("Choose your Address: ")
        res = requests.get(base_uri + list(addr_dict.values())[int(addr_index) + 1])
        soup = BeautifulSoup(res.content, "lxml")

    days_list = soup.findAll(name="div", attrs={"class": "collectionDay"})

    if len(days_list) == 0:
        return "Address not found, let me know of your address by typing addr: your_address"


    day_dict = {}
    for day in days_list:
    #    print(day.text)
        bins = day.findAll(name="div", attrs={"class": "title_short"})
        day_dict[day.find("h4").text] = [i.text for i in bins]
    # print(day_dict)


    if trash_type is not None:
        return_list = []
        for key, value in day_dict.items():
            if any(i for i in value if i.lower().startswith(trash_type[:4])):
                return_list.append(key)
        return return_list

    return day_dict


if __name__ == '__main__':
    getDates()
