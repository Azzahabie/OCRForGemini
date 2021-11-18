import cv2
import pytesseract


filteredList = []
keyItem = {

}

def filterStringToList(unfilteredString):
    for index, value in enumerate(unfilteredString):
        value = value.split(' ')
        if (len(value) != 1):
            print("adding to filteredList")
            filteredList.append(value)

def someFunction(listItem):
    i = 1
    for item in listItem:
        current_item = item
        keyItem[i] = {
            'date': current_item[0],
            'time': current_item[1],
            'coin': current_item[2],
            'buy/sell': current_item[3],
            'pricePerCoin': current_item[5],
            'price': current_item[7],
            'cost': current_item[8],
        }
        i += 1

# setting configs
pytesseract.pytesseract.cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
img = cv2.imread('helloWorld.png')
img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

img_to_string = pytesseract.image_to_string(img)
string_split = img_to_string.splitlines()

filterStringToList(string_split)
someFunction(filteredList)
print(keyItem)





