import sqlite3
from car_class import Car


conn=sqlite3.connect('car_records.db')
c=conn.cursor()

###---Initializing the table---###

c.execute("""CREATE TABLE car_records(carmake text, 
carmodel text, 
horsepower integer, 
carweight integer, 
zerotosixtytime float)""")

def insert_car(car):
    with conn:                                        ###---This is a context manager, which basically allows us to make commits without the need for us to then close them later. It does it automatically ### 
        c.execute("INSERT INTO car_records VALUES (:carmake, :carmodel, :horsepower, :carweight, :zerotosixtytime)", {'carmake': car.make, 'carmodel': car.model, 'horsepower': car.hrspr, 'carweight':car.weight, 'zertosixtytime':car.accel})

def get_cars_by_model(carmodel):
    c.execute("SELECT * FROM employees WHERE carmodel=:carmodel", {'carmodel': carmodel}) ###---SELECT does not need to be committed, so this does not need a context manager like everything else ### 
    return c.fetchone()

car_1= Car('Mazda', 'Miata', 181, 2341, 5.7)
car_2= Car('Subaru', 'STI', 315, 3370, 4.4 )

insert_car(car_1)
insert_car(car_2)

carlist=(get_cars_by_model('STI'),get_cars_by_model('Miata'))
print(carlist)

conn.commit()
conn.close()
