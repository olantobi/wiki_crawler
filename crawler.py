from bs4 import BeautifulSoup, Tag
import requests
import pymysql

Host = 'localhost'
User = 'root'
Password = 'root'
database = 'global_search_engine'

wikiUrl = 'https://en.wikipedia.org/wiki/List_of_time_zones_by_country';

page = requests.get(wikiUrl)
soup = BeautifulSoup(page.content, 'html.parser')

timezoneTable = soup.findChild('table')

conn  = pymysql.connect(host=Host, user=User, password=Password, database=database)
  
# Create a cursor object 
cur  = conn.cursor() 

data = []
for row in timezoneTable.findAll('tr'):
    dataColumns = row.findChildren('td')
    if not dataColumns:
        continue
    country = dataColumns[0]
    flag = country.findChild('span').findChild('img').get('src')
    countryName = country.findChild('a').getText()
    
    timezone = dataColumns[2].findChildren('a')[0].getText()
    print(countryName, timezone) 
    query = f"INSERT IGNORE INTO country_timezones (country_name, timezone) VALUES ('{countryName}', '{timezone}')"
    cur.execute(query);

    for brTag in dataColumns[2].findAll('br'):        
        nextSibling = brTag.nextSibling

        while not isinstance(nextSibling, Tag) and nextSibling is not None:
            nextSibling = nextSibling.nextSibling        

        if nextSibling is None:
            continue

        timezone = nextSibling.getText().replace('±', '+')

        print(countryName, timezone)  
        query = f"INSERT IGNORE INTO country_timezones (country_name, timezone) VALUES ('{countryName}', '{timezone}')"
        cur.execute(query);          

conn.commit()
conn.close()