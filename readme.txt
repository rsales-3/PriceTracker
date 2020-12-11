Don't you wish you could know if the discount price is really a good discount or not???
with this script our ultimate goal is:
Figure out if a deal is really a GOOD deal by comparing prices historical !

The main script {priceTracker.py}:
    -scrapes an Amazon item's URL for the item price. 
    -compares current price to a previously recorded price (if previously scrapped)
    -saves the price on the date the data was scrapped into a csv file (to later compare)

Two ways to run the script:

    Here is the syntax for a single itemname and it's url:
        python3 priceTracker.py productName productUrl

    Another way is run a separate python script that reads a txt file:
        python3 runTxtFile.py
    
    The txtfile name at the moment is hardcoded to be "items.txt" where the items must be formatted like so:
        ItemName(will be name of the csv file), URL

things to add/improve:
-function scans the csv file for the all time low price to THEN compare against the web scrapped price -- to see if the item is at an all time low
-could maybe append an arrow or something to signify that that time that the item was scrapped was the lowest
for example:
On 12/12/2020 at 14:00:00, Price: $200.00
On 13/12/2020 at 14:00:00, Price: $180.00 <--
On 14/12/2020 at 14:00:00, Price: $200.00

CURRENTLY, in our checking/comparing of prices we ONLY compare the current scrapped price to the previously saved scrapped price.

-Build a separate script that interactively creates a txt file to have the program read from...basically a CRUD - create wishlist
By building a .txt file and appending to it accordingly by user input (adding new item to track)
the .txt file is the database of items to track (higher level) that hide the lower level of results (csv files)

-create a price per count functionality... e.g. 25 count of boxes sell for 11.68... how much is that per box???
-create a feature that tells you when an item is on sale, and show the price it was originally
-a script that takes input and writes to the items.txt (wishlist)
-a script that takes input and scrapes the item "automatically" -searches for it...need to validate if it's the correct one however...
-beautify the output (make the csv files into pretty tables to display on a website? app?)