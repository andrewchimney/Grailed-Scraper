import psycopg2
import matplotlib.pyplot as plt
import statistics

class grail():
     def __init__(self, grail_tuple):
        self.id = grail_tuple[0]
        self.username = grail_tuple[1]
        self.designer = grail_tuple[2]
        self.price = grail_tuple[3]
        self.description = grail_tuple[4]
        self.sub_title =grail_tuple[5]
        self.link = grail_tuple[6]
        self.size = grail_tuple[7]
        self.color =grail_tuple[8]
        self.condition = grail_tuple[9]
def truncate_table():
    with conn:
        with conn.cursor() as curs:
            
        
            curs.execute(
                "TRUNCATE grails;"
                )
        conn.commit()
def get_table_data():
    grails=[]
    with conn:
        with conn.cursor() as curs:
            
        
            curs.execute(
                "SELECT * FROM grails;"
                )
            for record in curs:
                grails.append(grail(record))
        conn.commit()
    return grails
def insert():
    with conn.cursor() as curs:
        curs.execute("INSERT INTO grails(username, designer, price, description, sub_title, link, size, color, condition) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);",
            ('username','designer',1,'description','sub_title','link','size','color','condition'))
        conn.commit()
def create_table():
    with conn.cursor() as curs:
            curs.execute(
                """CREATE TABLE grails(
                         id int NOT NULL UNIQUE,
                         username varchar, 
                         designer varchar,
                         price INT,
                         description varchar,
                         sub_title varchar,
                         link VARCHAR,
                         size VARCHAR,
                         color VARCHAR,
                         condition VARCHAR);"""
                )
    conn.commit()


def graphConditions(grails):
    conditions=[]
    for g in grails:
         conditions.append(g.condition)
    n = float(conditions.count("New"))
    g = float(conditions.count("Gently Used"))
    u = float(conditions.count("Used"))
    w = float(conditions.count("Worn"))
    n = float(conditions.count("Not Specified"))
    data ={"New":n, "Gently Used":g, "Used":u, "Worn":w, "Not Specified":n}
    plt.bar(data.keys(),data.values())
    plt.xlabel("Conditions")
    plt.ylabel("Number")
    plt.title("Conditions Chrome Hearts Bags on Grailed")
    plt.show()

def graphPrice(grails):
    prices=[]
    for g in grails:
        prices.append(g.price)
    plt.boxplot(prices)
    average = statistics.mean(prices)
    median = statistics.median(prices)
    print(average)
    print(median)
    plt.xlabel("Bags")
    plt.ylabel("Price usd")
    plt.title("Boxplot of Prices of Chrome Hearts Bags on Grailed")
    plt.show()
    
conn = psycopg2.connect(dbname="databased", user="postgres", password="skippy123", port="5432", host="127.0.0.1")
#insert()
#grails = get_table_data()
#print(len(grails))
#graphPrice(grails)
#graphConditions(grails)
#create_table()
#truncate_table()
     