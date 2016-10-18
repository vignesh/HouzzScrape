from bs4 import BeautifulSoup
import urllib2

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
print "These are the top results for your search."
counter = 0
houzzData = {}
for houzzItem in houzzItems:
    counter +=1;
    houzzLink = houzzItem.a["href"]
    houzzLink = str(houzzLink)
    houzzLink = houzzLink.split("/")
    houzzId = houzzLink[4]
    houzzTitle = houzzLink[5];
    houzzData[counter] = houzzId
    #print counter
    #print houzzId
    print ("%d. %s") % (counter, houzzTitle)
    #houzzLink = houzzItem.findChildren()[0].findChildren()[0].findChildren()[0]
    #houzzTitle = houzzItem.findChildren()[0]

choice = (raw_input("Which of the results do you want breakdown? "))
choice = int(choice)

url = "http://www.houzz.com/photos/" + houzzData[choice]
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
                interiorCounter +=1
        except IndexError:
            houzzSubPrice = "Similar interior design"
            similarDesigns +=1
    except IndexError:
        houzzSubLen = -1
        houzzSubPrice = "Similar interior design"
        similarDesigns +=1
    # houzzSubPrice = houzzSubItem.findChildren()[1]
    """if (len(houzzSubItem.findChildren()) > 0):
        houzzSubPrice = houzzSubItem.findChildren()[1].findChildren()[0]
    else:
        houzzSubPrice = houzzSubItem.findChildren()[1]"""
    print ("%d. %s: %s") % (count, houzzSubTitle, houzzSubPrice)
print ("%d items depicted will cost $%d, %d similar Products, %d similar Designs.") % (interiorCounter, cost, similarProducts, similarDesigns)

