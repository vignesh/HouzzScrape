from bs4 import BeautifulSoup
import urllib2
import unicodedata
import re

search = (raw_input("1.Kitchen\n2.Bath\n3.Bedroom\n4.Living\n5.Outdoor\nWhat cateogory would you like to browse? "))
if search == '1':
    category = "kitchen"
elif search == '2':
    category = "bath"
elif search == '3':
    category = "bedroom"
elif search == '4':
    category = "living"
elif search == '5':
    category = "outdoor"
else:
    category = ""

url = "http://www.houzz.com/photos/" + category
content = urllib2.urlopen(url).read()
soup = BeautifulSoup(content, "html.parser")

houzzItems = soup.find_all('div', {'class': 'ic whiteCard xl portrait'})
print "\nThese are the top results for your search."
counter = 0
houzzData = {}
for houzzItem in houzzItems:
    counter +=1;
    houzzLink = houzzItem.a["href"]
    houzzLink = str(houzzLink)
    houzzLink = houzzLink.split("/")
    houzzId = houzzLink[4]
    houzzTitle = houzzLink[5];
    houzzData[counter] = (houzzId, houzzTitle)
    #print counter
    #print houzzId
    print ("%d. %s") % (counter, houzzTitle)
    #houzzLink = houzzItem.findChildren()[0].findChildren()[0].findChildren()[0]
    #houzzTitle = houzzItem.findChildren()[0]

choice = (raw_input("\nChoose an interior design for more details. "))
choice = int(choice)

url = "http://www.houzz.com/photos/" + houzzData[choice][0]
content = urllib2.urlopen(url).read()
soup = BeautifulSoup(content, "html.parser")
#print soup2.prettify()

houzzSubItems = soup.find_all('div', {'class': 'space-meta'})
#print houzzSubItems
count = 0
similarProducts = 0
similarDesigns = 0
interiorCounter = 0
cost = 0
for houzzSubItem in houzzSubItems:
    count +=1
    """houzzSubLink = houzzSubItem.a["href"]"""
    houzzSubTitle = houzzSubItem.findChildren()[0].get_text()
    try:
        houzzSubLen = len(houzzSubItem.findChildren()[1])
        try:
            houzzSubPrice = houzzSubItem.findChildren()[1].get_text()
            if houzzSubPrice[0] != "$":
                 houzzSubPrice = "Similar product"
                 similarProducts +=1
            else:
                sep = " "
                houzzSubPrice = houzzSubPrice.split(sep,1)[0]
                houzzSubPriceFloat = houzzSubPrice[1:]
                dec = "."
                houzzSubPriceFloat = houzzSubPriceFloat.split(dec,1)[0]
                #print type(houzzSubPriceFloat)
                houzzSubPriceFloat = unicodedata.normalize('NFKD', houzzSubPriceFloat).encode('ascii','ignore')
                #print type(houzzSubPriceFloat)
                houzzSubPriceFloat = houzzSubPriceFloat.replace(",", "");
                houzzSubPriceFloat = int(houzzSubPriceFloat)
                """floatvar = None
                    if re.match("^\d+?\.\d+?$", houzzSubPriceFloat) is None:
                    houzzSubPriceFloat = int(houzzSubPriceFloat)"""
                """if isinstance(houzzSubPriceFloat, str):
                    houzzSubPriceFloat = float(houzzSubPriceFloat)"""
                """else:
                    floatvar = float(houzzSubPriceFloat)
                print (type(floatvar))"""
                #print houzzSubPriceFloat
                #print type(houzzSubPriceFloat)
                cost += houzzSubPriceFloat
                interiorCounter +=1
        except IndexError:
            houzzSubPrice = "Similar interior design"
            similarDesigns +=1
    except IndexError:
        houzzSubLen = -1
        houzzSubPrice = "Similar interior design"
        similarDesigns +=1
    print ("%d. %s: %s") % (count, houzzSubTitle, houzzSubPrice)
print ("\nThere are %d items depicted in %s which was sum up to cost $%d. There are also %d similar products offered, and %d similar interior designs.") % (interiorCounter, houzzData[choice][1], cost, similarProducts, similarDesigns)

