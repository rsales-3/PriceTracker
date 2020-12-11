#Is there a way to traverse to a different website that holds the same item. 
# There was a situation where the website would say.. currently available elsewhere or currently available from other sellers???
from bs4 import BeautifulSoup
from datetime import datetime
import requests, time, sys

def main(arg1, arg2):
    productName = arg1
    link = arg2
    source = get_page_source(link)
    price = get_price(source)
    comparePrices(price,productName)
    save_history(productName,price)


def comparePrices(price, productName):
    #get previous price
    prevPrice = check_prev(productName).strip().replace('$','')
    #try converting
    if(':' in prevPrice): #if single digit price we have ": X.XX"...need to remove ':' in order to read/compare str
        prevPrice = prevPrice.replace(':','').strip()
    try:
        prevPrice = float(prevPrice)
    except:
        print(f"No previous price to compare against for {productName}.")
        return
    #Converting current price
    try:
        price = float(price.replace('$',''))
    except ValueError:
        print("Current price is unavailable")
        return
    #Comparing
    if(price < prevPrice):
        print("There is a reduction in price!")
    elif(price > prevPrice):
        print("There is an increase in price!")
    else:
        return


def get_page_source(link):
    headers = {
    'authority': 'www.amazon.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'rtt': '50',
    'downlink': '10',
    'ect': '4g',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
    'accept': 'image/avif,image/webp,image/apng,image/*,*/*;q=0.8',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-dest': 'image',
    'referer': 'https://www.amazon.com/NB32CW-32-Inch-Professional-Bezel-Less-FreeSync/dp/B07G6RNQVG/ref=sr_1_2_sspa?dchild=1&keywords=curved+monitor&qid=1605215073&sr=8-2-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUFOSDJYUzFWU1NDNE0mZW5jcnlwdGVkSWQ9QTA5Mzg0MzdHMFMyN04zSDIwS00mZW5jcnlwdGVkQWRJZD1BMDY2Mzk0NjFFMEUxOFBQVklXU0wmd2lkZ2V0TmFtZT1zcF9hdGYmYWN0aW9uPWNsaWNrUmVkaXJlY3QmZG9Ob3RMb2dDbGljaz10cnVl',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': 's_dslv_s=First%20Visit; s_depth=1; s_vn=1633492437393%26vn%3D1; s_invisit=true; regStatus=pre-register; aws-target-data=%7B%22support%22%3A%221%22%7D; aws-target-visitor-id=1601956437726-129396.35_0; s_dslv=1601956446777; s_nr=1601956446783-New; i18n-prefs=USD; ubid-main=134-6832456-6753959; ubid-acbus=130-2490445-9661138; x-main="OSYFAPEtnqAHrOLqkEIYNjs0l0DoJfQ1rs8yndby0GembJvDlcYG9OV2?nYijAtd"; at-main=Atza|IwEBIMv2cnyAvCWRG45S5IBdm_ADCSZbmhYlrPPBh5tOpENZrdkxozaBUhTj5mtPuknS83sEmU3CLSQrWEq5-UZPLmpMEICRDILZa3x734BULkcZ6YXigc2I-lMc9PHknfcQZJmtUgeBg7KU9LFLwDNRM7ZLBraoz_Bh9v2arPQe98IJVA49vzM277jtQTMaDBcZaEJ1avE5uefJzmp2KR9Qzs9I1YeuK5y1ojSY-yvKMgfaPQ; sess-at-main="COfsXNOQQ6VJAhCr9Kewxa7G2lbskl0tLU0d+rZVzPE="; sst-main=Sst1|PQGjzbFw927qMG3wXNvc9af1CRjLEMPDi25yjOCi_svfV48_kYuSV1vj4XfPL66InwplebLVjkeRfzL_VXv7gG53GVReESmu30hvxeL1U-X4ufG9om02kfA4d9AA1cLvgNdjPv-Q9d6ZktoLvSq1tbnQLkXV8CxgNgi5I5JV0uAhRbybNyhkRFw9YppYODZIPwY37KbbcQe1R12gZ35XqLs_fihruzWyBdAGKpcH0ccb4zyeW3ffl16brEz3hiV3ShO3OzlL5KxEysZZXARPq9D_HssgNgPgx17NxW7ikHACz2Y; session-id-time=2082787201l; s_pers=%20s_fid%3D6A0F6CDC5350D5EF-0164CF712FD6A238%7C1761002617319%3B%20s_dl%3D1%7C1603238017322%3B%20gpv_page%3DUS%253ASD%253ASOA-learn%7C1603238017330%3B%20s_ev15%3D%255B%255B%2527SCSOAlogin-learn%2527%252C%25271603077451552%2527%255D%252C%255B%2527SEUSSOAGOOG-B10000-D%2527%252C%25271603077460773%2527%255D%252C%255B%2527NSGoogle%2527%252C%25271603236217357%2527%255D%255D%7C1761002617357%3B; session-id=144-4272248-0323556; session-token="AMnCDI/Til7Yy5maPcdKcsnVWl2mUogJTWYmKzsmefNgnw/7AAjuXoIbTl12wFHt3YEz3SWD7vgR7zl0E/PcOGriCsgHAN4WigaTvRMVyfTBvMqxv+Dpza+IJBZw5kB3HoGyc+JaZNW+gl6wEujdtRFYP3IVSjrnrGS2oUqAFj2/PJFLDj6GQ01EWvx6q/Lp1fXCAZowOGPXZkpL1j8PvA=="; skin=noskin; csm-hit=tb:s-ZY7QDXXZ6A1XGADM0TYV|1605216321630&t:1605216321630&adb:adblk_no',
    }

    params = (
        ('dchild', '1'),
        ('keywords', 'curved monitor'),
        ('qid', '1605215073'),
        ('sr', '8-2-spons'),
        ('psc', '1'),
        ('spLa', 'ZW5jcnlwdGVkUXVhbGlmaWVyPUFOSDJYUzFWU1NDNE0mZW5jcnlwdGVkSWQ9QTA5Mzg0MzdHMFMyN04zSDIwS00mZW5jcnlwdGVkQWRJZD1BMDY2Mzk0NjFFMEUxOFBQVklXU0wmd2lkZ2V0TmFtZT1zcF9hdGYmYWN0aW9uPWNsaWNrUmVkaXJlY3QmZG9Ob3RMb2dDbGljaz10cnVl'),
    )

    response = requests.get(link, headers=headers, params=params)

    return response.text


def get_price(source):
    price_element_id = "priceblock_ourprice"
    soup = BeautifulSoup(source, "lxml")    
    price = soup.find('span', id=price_element_id)
    try:
        return price.text
    except AttributeError:
        price = soup.find('span', id="priceblock_dealprice") 
        if(price == None):
            price = soup.find('span', id="priceblock_saleprice")
            if(price == None):
                try:
                    msg = soup.find('span', attrs={'class':'a-size-medium a-color-price'}).text.strip()
                    return msg
                except AttributeError:
                    print("ITEM IS UNAVAILABLE ON AMAZON.") #maybe a different area of the code I'll check if the item is there or not by verifying the name on the webpage
            else: #if it prints (Available from these sellers --> means Amazon isn't sell but other people selling ON amazon are...)
                return price.text #So then we'd want to get to that click potentially and list those prices??? wouldn't I wanna use selenium there?
        else:
            return price.text    


## Append to the top of the csv file???? -- https://www.xspdf.com/resolution/53028942.html

def save_history(productName, price):
    with open(f"data/{productName}.csv", "a") as file:
        print(f"Opening {productName}.csv")
        current_datetime = datetime.now().strftime("On %d/%m/%Y at %H:%M:%S")
        file.write(f"{current_datetime}, Price: {price}\n")
        print("Writing to csv file!")

def check_prev(productName):
    f = open(f"data/{productName}.csv", "r")
    f.seek(0,2)
    f.seek(f.tell() - 8, 0)
    return(f.read())




if __name__ == "__main__":
    if sys.argv[0] == "priceTracker.py": #this mean we're running main script with a product and it's url solely --> python3 priceTracker.py productName URL
        main(sys.argv[1],sys.argv[2]) 
        sys.exit() 
    main(sys.argv[0],sys.argv[1]) #Otherwise this will run when called by different script
    print("Check csv files for update!")

