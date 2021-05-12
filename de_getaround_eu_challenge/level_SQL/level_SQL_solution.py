import pandas as pd
import sqlite3

rentals = pd.read_csv("https://cl.ly/Wnuebn1m/download/rentals.csv")
cars = pd.read_csv("https://cl.ly/nOuzerJK/download/cars.csv")
cars.fillna(method="ffill", inplace=True)

create_cars = """
   CREATE TABLE IF NOT EXISTS CAR(
   id BIGINT PRIMARY KEY,
   city TEXT,
   created_at TEXT
   );"""
create_rentals = """
   CREATE TABLE IF NOT EXISTS RENTAL(
   id BIGINT PRIMARY KEY,
   car_id BIGINT,
   starts_at TEXT,
   ends_at TEXT,
   FOREIGN KEY (car_id) REFERENCES car (id) 
   );"""

conn = sqlite3.connect("pythonsqlite.db")

# Creating a cursor object using the cursor() method
cursor = conn.cursor()

# create car and rental table
cursor.execute(create_cars)
cursor.execute(create_rentals)
conn.commit()

sqlite_insert_car = """INSERT INTO CAR
                    (id, city, created_at) 
                    VALUES (?, ?, ?);"""
for row in cars.iterrows():
    data_tuple = (row[1]["id"], row[1]["city"], row[1]["created_at"])
    cursor.execute(sqlite_insert_car, data_tuple)
conn.commit()
print("car table done!")

sqlite_insert_rental = """INSERT INTO RENTAL
                    (id, car_id, starts_at, ends_at) 
                    VALUES (?, ?, ?, ?);"""
for row in rentals.iterrows():
    data_tuple = (
        row[1]["id"],
        row[1]["car_id"],
        row[1]["starts_at"],
        row[1]["ends_at"],
    )
    cursor.execute(sqlite_insert_rental, data_tuple)
conn.commit()
print("rental table done!")

key_sql = """ select car_id, count(id) as no_rental, 
substr(starts_at, 1, 4) as year_starts_at, 
substr(starts_at, 6, 2) as month_starts_at
from (
select car.id as car_id, rental.id, car.created_at,  rental.starts_at
from car, rental
where car.id = rental.car_id and date(car.created_at) <= date(rental.starts_at) )
group by year_starts_at, month_starts_at, car_id
having no_rental>=3;
"""

df = pd.read_sql_query(key_sql, con=conn)

print(f"{df.shape[0]} cars have been rented more than 3 times since inception")
