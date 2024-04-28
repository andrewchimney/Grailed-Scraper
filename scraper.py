import time 
import psycopg2
from selenium import webdriver
from selenium.webdriver.common.by import By
conn = psycopg2.connect(dbname="databased", user="postgres", password="skippy123", port="5432", host="database-1.chiyyamckstw.us-east-2.rds.amazonaws.com")
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:125.0) Gecko/20100101 Firefox/125.0'
options = webdriver.ChromeOptions() 
options.add_argument('user-data-dir=/Users/Andrew/Library/Application Support/Google/Chrome')
options.add_argument('--profile-directory=Profile 24')
options.add_argument('loadsImagesAutomatically initial=false')
options.add_argument('--blink-settings=imagesEnabled=false')
options.add_argument('--headless') 
options.add_argument("--window-size=1920,1080")
options.add_argument(f'user-agent={user_agent}')
driver = webdriver.Chrome(options=options)
Link =[]
scroll_count=0

driver.get("https://www.grailed.com/shop/M5M4fRml0g")

SCROLL_PAUSE_TIME = 3

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
    driver.save_screenshot('scroll.png')
    scroll_count+=1

results = driver.find_elements(by=By.XPATH, value='//a[@class="listing-item-link"]')
for result in results:
        Link.append(result.get_attribute("href"))

for link in Link:
    driver.get(link)
    driver.save_screenshot('item.png')
    try:
        driver.find_element(by=By.XPATH, value='//div[@class="Text Callout_callout__1Kvdw Fancy_message__uVdQ5"]').text
        id=link[33:41]
        if id[7]=="-":
            id=id[0:6]
        with conn.cursor() as curs:
            curs.execute("DELETE FROM grails WHERE id=%s", (id,))
            conn.commit()
    except Exception as e:
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
"""INSERT INTO grails(id, username, designer, price, description,sub_title, link,size, color, condition)
VALUES (60304042,'cd','Chrome Hearts',200,'Chrome Hearts Glasses Case Black Variation 100% Authentic No Returns/Refunds *Missing Dagger Zipper','Chrome Hearts Glasses','https://www.grailed.com/listings/60304072-chrome-hearts-chrome-hearts-glasses-case?g_aidx=Listing_production&g_aqid=8871e6fba87a4d32c6114dba8caf4b41','ONE SIZE','Black','Worn')
ON CONFLICT(id) DO UPDATE SET username='cd',designer='Chrome Hearts',price=201,description='des', sub_title='as',link='dfg',size='m',color='red',condition='d';
"""
driver.quit()

"""
starttime = time.monotonic()
while True:
    print("tick")
    with conn:
        with conn.cursor() as curs:
            
            curs.execute(" INSERT INTO grails (username, designer, price, description, sub_title, link, size, color, condition) VALUES (%s, %s, %s,%s, %s, %s,%s,%s,%s);",
        ("Haydensmith0968",300,"Chrome Hearts","asldfjalsdf","https://www.grailed.com/listings/59977498-chrome-hearts-chrome-hearts-giss-brown-glasses-demo-frames?g_aidx=Listing_sold_production&g_aqid=48e000c7490fe704ecf9e03a83fa173a","ONE SIZE","Gently Used"))
            
        
            curs.execute(
                "SELECT * FROM grails;"
                )
            for record in curs:
                print(record)
    conn.commit
    time.sleep(10 - ((time.monotonic() - starttime) % 10))
    """
"""
with conn:
        with conn.cursor() as curs:
            
            curs.execute("CREATE TABLE grails(
                         id INT GENERATED ALWAYS AS IDENTITY, 
                         username varchar, 
                         designer varchar,
                         price INT,
                         description varchar,
                         sub_title varchar,
                         link VARCHAR,
                         size VARCHAR,
                         color VARCHAR,
                         condition VARCHAR);")
            #for record in curs:
            #   print(record)
            #conn.commit()
            """
"""CREATE TABLE grails(
                         id INT GENERATED ALWAYS AS IDENTITY, 
                         username varchar, 
                         designer varchar,
                         price INT
                         description varchar,
                         sub_title varchar,
                         link VARCHAR,
                         size VARCHAR,
                         color VARCHAR,
                         condition VARCHAR);"""