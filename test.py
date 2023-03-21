from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import re
import os

stores = ['zonafresca.com', 'zionmarket.com', 'zerossub.com', 'zeppes.com', 'zazacubancomfort.com', 'zaoasiancafe.com', 'zakkushi.com', 'zabas.com', 'yummyhouseflorida.com', 'yumkitchen.com', 'yumilicious.co', 'yourpie.com', 'yoshiharuramen.com', 'yogenfruz.com', 'ymyusa.com', 'yifangteausa.com', 'yeehawbrewing.com', 'yayatea.com', 'xingfutang.ca', 'zuckersbagels.com', 'z-teca.com', 'zitospizza.com', 'zippys.com', 'zippssportsgrills.com', 'zerodegreescompany.com', 'zburger.com', 'zaxbys.com', 'zaro.com', 'zaoasiancafe.com', 'zanottos.com', 'yukdaejangusa.com', 'yourpie.com', 'yourfoodtown.com', 'yonutz.com', 'yongmoonlu.com', 'yogofina.com', 'yifangteapnw.com', 'yifangab.com', 'yellowpages.com', 'yboriginal.com', 'yateskingstownecarwash.com', 'yahsbest.com', 'wyndhamhotels.com', 'wushiland-usa.com', 'wrapcitysandwiches.com', 'wowmomsworld.com', 'woodntap.com', 'wolfnights.com', 'woknfire.com', 'wittenfarm.com']

driver = webdriver.Chrome()
pattern = re.compile(r'(\(|)\d{3}(.)( |)\d{3}(.)\d{4}')
url = 'https://www.google.com/'
wait_time = 10
order = 1
store_data = {}

for store in stores:
    phone_numbers = set()
    driver.get(url)

    # Search store through Google
    search_box = driver.find_element(By.NAME, 'q')
    search_box.send_keys(store + ' locations')
    search_box.send_keys(Keys.RETURN)

    # Verify CAPTCHA
    while True:
        try:
            # Click first result
            first_result = driver.find_element(By.CSS_SELECTOR, 'span.VuuXrf')
            first_result.click()
            break
        except:
            continue

    # Extract phone-numbers
    time.sleep(5)
    elements = driver.find_elements(By.XPATH, "//*[text()[contains(., '0') or contains(., '1') or contains(., '2') or contains(., '3') or contains(., '4') or contains(., '5') or contains(., '6') or contains(., '7') or contains(., '8') or contains(., '9')]]")
    for element in elements:
        text =  element.text  if element else ''
        match = re.search(pattern, text)
        if match:
            phone_numbers.add(match.group())
    
    # Persist store numbers
    store_num = len(phone_numbers)
    store_data[store] = store_num
    print(f'{order}) {store}: {store_num}')
    order += 1

driver.quit()

# Output results in JSON file
file_name = 'results.json'
df = pd.DataFrame.from_dict([store_data])
if os.path.isfile(file_name):
    os.remove(file_name)
df.to_json(file_name, orient='records')  

'''
Number formats allowed:
    123-456-7890
    (123) 456-7890
    123 456 7890
    123 456-7890
    123.456.7890
'''