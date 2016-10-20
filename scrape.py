from bs4 import BeautifulSoup
import urllib2
import unicodedata

#ask user for category
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

#create and oepn new URL
url = "http://www.houzz.com/photos/" + category
content = urllib2.urlopen(url).read()
soup = BeautifulSoup(content, "html.parser")

print "\nThese are the top results for your search."
houzzItems = soup.find_all('div', {'class': 'ic whiteCard xl portrait'})
counter = 0
houzzData = {}
for houzzItem in houzzItems:
    counter +=1; #counter for dictionary index
    houzzLink = houzzItem.a["href"] #grab href link
    houzzLink = houzzLink.split("/") #split Link by '/'
    houzzId = houzzLink[4]
    houzzTitle = houzzLink[5];
    houzzTitle = houzzTitle.replace('-',' ') #replace '-' with space
    houzzTitle = houzzTitle.title() #capitalize first character in every word
    houzzData[counter] = (houzzId, houzzTitle) #at counter index insert a tuple with id and title
    print ("%d. %s") % (counter, houzzTitle)

#ask user for interior choice
choice = (raw_input("\nChoose an interior design for more details. "))
choice = int(choice)

#create new link for interior
url = "http://www.houzz.com/photos/" + houzzData[choice][0]
content = urllib2.urlopen(url).read()
soup = BeautifulSoup(content, "html.parser")

#finds all items on page
houzzSubItems = soup.find_all('div', {'class': 'space-meta'})
count = 0
similarProducts = 0
similarDesigns = 0
interiorCounter = 0
cost = 0
for houzzSubItem in houzzSubItems:
    count +=1
    houzzSubTitle = houzzSubItem.findChildren()[0].get_text() #grab item title
    try:
        houzzSubLen = len(houzzSubItem.findChildren()[1]) #check if there is a child
        try:
            houzzInfo = houzzSubItem.findChildren()[1].get_text()
            if houzzInfo[0] != "$": #check if first letter is a '$'
                 houzzInfo = "Similar product"
                 similarProducts +=1 #increase similar products
            else:
                space = " "
                houzzInfo = houzzInfo.split(space,1)[0] #remove all characeters after a space
                houzzSubPrice = houzzInfo[1:] #removes first character
                decimal = "."
                houzzSubPrice = houzzSubPrice.split(decimal,1)[0] #remove charceters after decimal
                houzzSubPrice = unicodedata.normalize('NFKD', houzzSubPrice).encode('ascii','ignore') #convert unciode to string
                houzzSubPrice = houzzSubPrice.replace(",", ""); #remove commas
                houzzSubPrice = int(houzzSubPrice) #convert string to float
                cost += houzzSubPrice #add product price to total cost
                interiorCounter +=1 #increase interior counter
        except IndexError:
            houzzInfo = "Similar interior design"
            similarDesigns +=1 #increase similar design counter
    except IndexError:
        houzzInfo = "Similar interior design"
        similarDesigns +=1 #increase similar design counter
    print ("%d. %s: %s") % (count, houzzSubTitle, houzzInfo)
print ("\nThere are %d items present in %s which sum up to a total cost of $%d. There are also %d similar products offered, and %d similar interior designs.") % (interiorCounter, houzzData[choice][1], cost, similarProducts, similarDesigns)
