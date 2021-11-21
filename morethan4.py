import cv2
import pytesseract
from re import sub
import re
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
startIndex = 0
rowAndColumnList = []

# takes in unfilteredString from image scan -> filter out empty values -> find start index of non date to determine
# the amount of rows there are in the image
def filter_imgstring_to_list(unfilteredString):
    pattern = '\d\d\/\d\d\d\d'
    foundindex = False
    for index, value in enumerate(unfilteredString):
        if (re.search('[a-zA-Z0-9]', value)):
            currentword = re.findall(pattern, value)
            if (len(currentword) == 0 and foundindex is False):
                foundindex = True
                global startIndex
                startIndex = int(index / 2)
            filteredList.append(value)


#  Tn = a + (n-1)d; can get any value from image with row and column
def math_shit(column, row):
    index = row + (column - 1) * startIndex
    return index

# places items into list where each item in list is a row in the image
def iterate_shit():
    for i in range(startIndex):
        templist = []
        for x in range(1, 9):
           templist.append(filteredList[math_shit(x,i)])
        rowAndColumnList.append(templist)


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
            if (value == 'coin'):
                if (list[item]['buy/sell'] == 'Buy'):
                    buycount += 1
                    buykey = sortby_type_dict['buy']
                    buykey[buycount] = list[item]
                else:
                    sellcount += 1
                    sellkey = sortby_type_dict['sell']
                    sellkey[sellcount] = list[item]


def calculate_total_by_type(dict, type):
    tempTotal = 0
    if (type == 'buy'):
        for item in dict:
            for index, value in enumerate(dict[item]):
                tempindex = dict[item]
                if (value == 'cost'):
                    converted_cost = Decimal(sub(r'[^\d.]', '', tempindex[value]))
                    tempTotal += converted_cost
        return tempTotal

    if (type == 'sell'):
        for item in dict:
            for index, value in enumerate(dict[item]):
                tempindex = dict[item]
                if (value == 'cost'):
                    converted_cost = Decimal(sub(r'[^\d.]', '', tempindex[value]))
                    tempTotal += converted_cost
        return tempTotal


def getImage():
    print("Available Sample: 2lines, 3lines, 4lines, wide2, wide3, wide4, bigsample")
    userinput = input("Pick Sample: ")
    link = f"./sampleImages/{userinput}.png"
    print(link)
    return link


def printResults():
    print(f"Net Profit / Loss:  \n${netProfit}")
    print(f"Net Profit Margin / loss:  \n{round(netProfitMargin, 2)}%")
    print(f"Profit Percentage / loss: \n{round(profitPercentage, 2)}%")


# ---------------------------------------MAIN CODE?------------------------------------------

# setting configs
pytesseract.pytesseract.cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
img = cv2.imread('./sampleImages/bigsample.png')
img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

img_to_string = pytesseract.image_to_string(img)
imgString_Split = img_to_string.splitlines()

# functions calling my mom
filter_imgstring_to_list(imgString_Split)
iterate_shit()
print(rowAndColumnList)