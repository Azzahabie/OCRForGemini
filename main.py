import cv2
import pytesseract
from re import sub
from decimal import Decimal

# list if transaction after being filtered
filteredList = []
# creates a key value pair with transactions as value broken down
key_value_dict = {

}
# stores key_value_dict into a buy / sell dict
sortby_type_dict = {
    'buy': {

    },
    'sell': {

    }

}

# takes in string obtain from openCV and put into list???
def filter_string_to_list(unfilteredString):
    for index, value in enumerate(unfilteredString):
        value = value.split(' ')
        if (len(value) != 1):
            #print("adding to filteredList")
            filteredList.append(value)

# take filteredList and breaks down into dict
def insert_into_dict(listItem):
    i = 1
    for item in listItem:
        current_item = item
        key_value_dict[i] = {
            'date': current_item[0],
            'time': current_item[1],
            'coin': current_item[2],
            'buy/sell': current_item[3],
            'pricePerCoin': current_item[5],
            'coins': current_item[7],
            'cost': current_item[9],
        }
        i += 1

# takes dict and sorts it into buy / sell dict
def sort_by_type(list):
    buycount = 0
    sellcount = 0
    for item in list:
        for index, value in enumerate(list[item]):
            if(value == 'coin'):
                if(list[item]['buy/sell'] == 'Buy'):
                    buycount += 1
                    buykey = sortby_type_dict['buy']
                    buykey[buycount] = list[item]
                else:
                    sellcount += 1
                    sellkey = sortby_type_dict['sell']
                    sellkey[sellcount] = list[item]

def calculate_total_by_type(dict, type):
    tempTotal = 0
    if(type == 'buy'):
        for item in dict:
            for index,value in enumerate(dict[item]):
                tempindex = dict[item]
                if(value == 'cost'):
                    converted_cost = Decimal(sub(r'[^\d.]', '', tempindex[value]))
                    tempTotal += converted_cost
        return tempTotal

    if(type == 'sell'):
        for item in dict:
            for index,value in enumerate(dict[item]):
                tempindex = dict[item]
                if(value == 'cost'):
                    converted_cost = Decimal(sub(r'[^\d.]', '', tempindex[value]))
                    tempTotal += converted_cost
        return tempTotal

def getImage():
    print("Available Sample: 2lines, 3lines, 4lines, wide2, wide3, wide4, bigsample")
    userinput = input("Pick Sample: ")
    link = f"./sampleImages/{userinput}.png"
    print(link)
    return link



# setting configs
pytesseract.pytesseract.cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
img = cv2.imread(getImage())
img = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)

img_to_string = pytesseract.image_to_string(img)
string_split = img_to_string.splitlines()

# functions calling my mom
filter_string_to_list(string_split)
insert_into_dict(filteredList)
sort_by_type(key_value_dict)
cost = calculate_total_by_type(sortby_type_dict['buy'], 'buy')
revenue = calculate_total_by_type(sortby_type_dict['sell'], 'sell')

netprofit = revenue - cost
netprofitmargin = netprofit / revenue

print(netprofit)
print(netprofitmargin)






