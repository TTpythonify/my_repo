from bs4 import BeautifulSoup
import requests, time
from api_key import my_api_key

def find_price():
    # WEBPAGE URL
    url = ('https://www.lilienthal.berlin/en/l01-121-cb044es'
           '?voucher=special&trc_gcmp_id=17485481751&trc_gag_id='
           '&trc_gad_id=&utm_source=Google&gad_source=1&'
           'gclid=Cj0KCQjwwYSwBhDcARIsAOyL0fjhpwCC1jrI_bcT2DXroMEF2FbKReMO1N-M_E_'
           'RHgf3IT7BX_TfU4caAuoaEALw_wcB')
    
    response = requests.get(url)
    
    # Check if the page was retrieved successfully
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None

    # Parse the page using BeautifulSoup
    page = BeautifulSoup(response.text, 'html.parser')

    # Find the price element
    span = page.find('span', class_="price--content content--default")
    if not span:
        print("Price element not found.")
        return None
    
    price_of_watch = span.text.strip()  # Output example: '145.56 $'
    
    try:
        amount = float(price_of_watch.split()[0]) 
    except ValueError:
        print("Failed to convert the price to a number.")
        return None
    
    return amount
"""
This is my comments that i want to use to demonstrate the advantages of using github for programmers

"""

# Send a notification using the Pushbullet API
def send_notification(title, body, api_key):
    url = 'https://api.pushbullet.com/v2/pushes'
    headers = {'Access-Token': api_key}
    data = {
        'type': 'note',
        'title': title,
        'body': body
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print("Notification sent successfully!")  # Debugging purposes
    else:
        print(f"Failed to send notification. Status code: {response.status_code}")

def check_price():
    price = find_price()
    
    if price is None:
        print("Could not retrieve the price.")
        return

    # Check if the watch price is less than 140
    if price < 140: 
        send_notification("Price Alert", "Item is now at a perfect price to purchase!", my_api_key)
    else:
        print(f"Not the right time yet. Current price is {price}")

# Run the scheduler
while True:
    check_price()
    # Check every 24 hours 
    time.sleep(24 * 60 * 60)
