import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
#setup
all_page_urls = []
all_listing_data=[]
driver=webdriver.Chrome()
current_url = "https://www.daraz.lk/laptops/?page=1&price=50000-&sort=priceasc"
driver.get(current_url)
wait=WebDriverWait(driver,10)
#i did some research on the webpage and identified that most of the time in item description the currentprice takes more time to load than the title
#so i added more waiting time to it
l_wait=WebDriverWait(driver,15)
print("Browser started. Giving it a moment to warm up and cache assets...")
# so i had cold start condition thats why i added this code for warmup
try:
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(3)
    print("Warm-up complete. Starting main scraping loop...")
except TimeoutException:
    print("Initial page load failed. Please check your internet connection and the URL.")
    driver.quit()
    exit() 

#use this loop to collect links first 
while True:
    print(f"Finding links on page: {driver.current_url}")
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div._17mcb")))
    listings = driver.find_elements(By.CSS_SELECTOR, "div.Bm3ON")
    for listing in listings:
        try:
            link = listing.find_element(By.TAG_NAME, "a").get_attribute("href")
            if link not in all_page_urls:
                all_page_urls.append(link)
        except NoSuchElementException:
            continue
    try:
        next_li_element = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "li.ant-pagination-next")))
        if next_li_element.get_attribute("aria-disabled") == "true":
            print("Next button is disabled. Reached the last page.")
            break 
        button_to_click = next_li_element.find_element(By.CSS_SELECTOR,"button.ant-pagination-item-link")
        driver.execute_script("arguments[0].click();", button_to_click)
        button_to_click.click()
        print("Navigating to next page...")
        time.sleep(2)
    except NoSuchElementException:
        print("Could not find the 'Next' button. Scraping finished.")
        break
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        break

print(f"Finished collecting links. Found {len(all_page_urls)} total listings.")
#after some research in the site i identifed that most sellers dont added the brand so thought of getting name by their titles
#because in most product titles they included the brand of the item
BRAND_KEYWORDS = {
    'HP': ['hp', 'pavilion', 'envy', 'spectre', 'elitebook', 'probook', 'omen'],
    'Dell': ['dell', 'inspiron', 'xps', 'alienware', 'vostro', 'latitude'],
    'Lenovo': ['lenovo', 'thinkpad', 'ideapad', 'yoga', 'legion'],
    'Asus': ['asus', 'vivobook', 'zenbook', 'tuf', 'rog'],
    'Apple': ['apple', 'macbook', 'mac'],
    'MSI': ['msi'],
    'Acer': ['acer', 'aspire', 'predator'],
    'Razer': ['razer', 'blade']
}
def get_brand_from_title(title):
    """
    Infers the brand from a product title using a keyword dictionary.
    """
    title_lower = title.lower()
    for brand, keywords in BRAND_KEYWORDS.items():
        for keyword in keywords:
            if keyword in title_lower:
                return brand 
    return "Unspecified"
for url in all_page_urls:
    driver.get(url)
    print(f"Scraping details from: {url}")
    try:
        
        title = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "h1.pdp-mod-product-badge-title"))).text
        current_price=l_wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "span.notranslate.pdp-price.pdp-price_type_normal.pdp-price_color_orange.pdp-price_size_xl"))).text
        try:
          original_price = driver.find_element(By.CSS_SELECTOR, "span.notranslate.pdp-price.pdp-price_type_deleted.pdp-price_color_lightgray.pdp-price_size_xs").text
        except NoSuchElementException:
            original_price = "" 
        try:
            discount = driver.find_element(By.CSS_SELECTOR, "span.pdp-product-price__discount").text
        except NoSuchElementException:
            discount = "" 
        try:
           seller_rating = driver.find_element(By.CSS_SELECTOR, "a.pdp-link.pdp-link_size_s.pdp-link_theme_blue.pdp-review-summary__link").text
        except NoSuchElementException:
           seller_rating = "" 
        seller=l_wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"a.pdp-link.pdp-link_size_l.pdp-link_theme_black.seller-name__detail-name"))).text
        brand= get_brand_from_title(title)

        
        all_listing_data.append([title,current_price,original_price,discount,seller_rating,seller,brand])
        
    except (NoSuchElementException, TimeoutException):
        print(f"Could not find all details on {url}. Skipping.")
        continue
#creating the csv file and adding data
try:
    with open("daraz.csv","w",encoding="utf-8",newline="") as f:
        writer=csv.writer(f)
        writer.writerow(["title","current_price","original_price","discount","seller_rating","seller","brand"])
        if all_listing_data:
            writer.writerows(all_listing_data)
    print("succesfully saved to daraz.csv")
except Exception as e:
    print(f"error writing to file:{e}")
finally:
    driver.quit()

