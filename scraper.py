import time 
import psycopg2
from selenium import webdriver
from selenium.webdriver.common.by import By
conn = psycopg2.connect(dbname="databased", user="postgres", password="skippy123", port="5432", host="127.0.01")
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:125.0) Gecko/20100101 Firefox/125.0'
options = webdriver.ChromeOptions() 
options.add_argument('user-data-dir=/Users/Andrew/Library/Application Support/Google/Chrome')
options.add_argument('--profile-directory=Profile 24')
options.add_argument('loadsImagesAutomatically initial=false')
options.add_argument('--blink-settings=imagesEnabled=false')
#options.add_argument('--headless') 
options.add_argument("--window-size=1920,1080")
options.add_argument(f'user-agent={user_agent}')
driver = webdriver.Chrome(options=options)
Link =[]
scroll_count=0

PAGE_TO_SCRAPE= "https://www.grailed.com/designers/chrome-hearts/bags-luggage"
SCROLL_PAUSE_TIME = 3



driver.get(PAGE_TO_SCRAPE)


last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
    driver.save_screenshot('./pictures/scroll.png')
    scroll_count+=1

results = driver.find_elements(by=By.XPATH, value='//a[@class="listing-item-link"]')
for result in results:
        Link.append(result.get_attribute("href"))

for link in Link:
    driver.get(link)
    driver.save_screenshot('./pictures/item.png')
    try:
        #checks to make sure the item isn't sold
        driver.find_element(by=By.XPATH, value='//div[@class="Text Callout_callout__1Kvdw Simple_message__RkJl_"]').text
        id=link[33:41]
        if id[7]=="-":
            id=id[0:6]
        with conn.cursor() as curs:
            curs.execute("DELETE FROM grails WHERE id=%s", (id,))
            conn.commit()
    except Exception as e:
        time.sleep(1)
        username = driver.find_element(by=By.XPATH, value='//span[@class="Text Subhead_subhead__70fsG UsernameWithBadges_usernameText__ookiK"]').text
        designers = driver.find_elements(by=By.XPATH, value='//a[@class="Designers_designer__quaYl"]')
        designer=''
        for p in designers:
            designer+= p.text
            designer+= "×"
        designer=designer[0:-1]
        price = driver.find_element(by=By.XPATH, value='//div[@class="MainContent_item__PIrxq MainContent_price__RSyWC"]/div/span').text
        price = int(price[1:])
        descriptions = driver.find_elements(by=By.XPATH, value='//p[@class="Body_body__dIg1V Text Description_paragraph__Gs7y6"]')
        description =''
        for p in descriptions:
            description+= p.text
        sub_title = driver.find_element(by=By.XPATH, value='//h1[@class="Body_body__dIg1V Text Details_title__PpX5v"]').text
        details = driver.find_elements(by=By.XPATH, value='//p[@class="Body_body__dIg1V Text Details_detail__J0Uny Details_nonMobile__AObqX"]')
        size ='Not specified'
        color= 'Not Specified'
        condition='Not Specified'
        for d in details:
            if d.text[0:4]=='Size':
                size = d.text[5:]
            elif d.text[0:5]=='Color':
                color = d.text[6:]
            elif d.text[0:9]=='Condition':
                condition = d.text[10:]
        print(username)
        id=link[33:41]
        if id[7]=="-":
            id=id[0:6]
        with conn.cursor() as curs:
            curs.execute("""INSERT INTO grails(id,username, designer, price, description, sub_title, link, size, color, condition) 
                        VALUES (%s, %s, %s,%s, %s, %s,%s,%s,%s,%s)
                        ON CONFLICT(id) DO UPDATE SET username=%s,designer=%s,price=%s,description=%s, sub_title=%s,link=%s,size=%s,color=%s,condition=%s;""",
            (id,username,designer,price,description,sub_title,link,size,color,condition,username,designer,price,description,sub_title,link,size,color,condition))
            conn.commit()
