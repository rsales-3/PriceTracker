#this script runs priceTracker with a txt file loaded with items already.
#The txt file should be formatted like this:
#{itemname}, {url}
import priceTracker

with open("items.txt", "r") as file:
    lines = file.readlines()
    for line in  lines:
        line = line.strip()
        name, link = line.split(",")

        priceTracker.main(name, link)
        #source = priceTracker.get_page_source(link)
        #price = priceTracker.get_price(source)
        #priceTracker.save_history(name,price)