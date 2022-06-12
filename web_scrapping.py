import requests
from bs4 import BeautifulSoup
from datetime import datetime,date
import mysql.connector

mysqldb = mysql.connector.connect(host="localhost",user="root",password="password",database="students")
cursor = mysqldb.cursor()

# Create an URL object
url = 'https://en.wikipedia.org/wiki/List_of_prime_ministers_of_India'
# Create object page
page = requests.get(url)
# parser-lxml = Change html to Python friendly format
# Obtain page's information

soup = BeautifulSoup(page.text, 'html.parser')

league_table = soup.find('table', class_ = 'wikitable')

for team in league_table.find_all('tbody'):
    rows = team.find_all('tr')
    minister_lst=[]
    for row in range(len(rows)):
        j=row+1
        value=rows[row].find_all('td')

        valp=[dp.text.strip() for dp in value]

        if len(valp) > 6:
            minister_lst.append(valp)

for i  in range(len(minister_lst)):
    j=i+1

    for val in range(len(minister_lst[i])):
        name = minister_lst[i][2]
        took = minister_lst[i][4].strip('[§]')
        if minister_lst[i][-1] == '':
            party = minister_lst[i][-2]
    if j == len(minister_lst):
        today = date.today()
        left =today.strftime("%d %B %Y")

    else:
        for valu in range(len(minister_lst[j])):
            left = minister_lst[j][4].strip('[§]')

    took = datetime.strptime(took, '%d %B %Y')
    took = took.date()
    left = datetime.strptime(left, '%d %B %Y')
    left = left.date()


    #create table
    create_qry="CREATE TABLE if not exists primeministers (Name VARCHAR(50),Party VARCHAR(50),TookOffice DATE, " \
               "LeftOffice DATE)"
    cursor.execute(create_qry)

    #insert query
    qry=f"insert into primeministers values('{name}','{party}','{took}','{left}')"

    cursor.execute(qry)
    mysqldb.commit()


#1. Write a query to sum the total time in office of each of the prime minister
print("#1. Write a query to sum the total time in office of each of the prime minister")

qry2="SELECT  Name,tookoffice, leftoffice,sum(DATEDIFF (leftoffice,tookoffice ))  AS days FROM primeministers " \
     "group by Name"

cursor.execute(qry2)
myresult = cursor.fetchall()
for x in myresult:
  print(x)


#2. Number of tenures each one resided in office.
print("\n#2. Number of tenures each one resided in office.")

qry3="select name,count(Name) as numberoftimes FROM primeministers group by name "

cursor.execute(qry3)
myresult = cursor.fetchall()
for x in myresult:
  print(x)


#3. List the 3 rd highest tenure(total time in office) prime minister.
print("\n#3. List the 3 rd highest tenure(total time in office) prime minister.")

qry4="SELECT  Name,tookoffice, leftoffice,sum(DATEDIFF (leftoffice,tookoffice ))  AS days FROM primeministers " \
     "group by Name order by days desc limit 2,1"

cursor.execute(qry4)
myresult = cursor.fetchall()
for x in myresult:
  print(x)