import sqlite3
from car import Car
from cars_sql_scheme import create_table_cars, create_table_repairs


"""Represents a sample car.

    Arguments:
    make - car make e.g. Honda
    model - car model e.g. Civic
    year - year of production
    vrn - vehicle registration number
    vin - VIN number
    sold - if car is still our property
"""


class Helper():
    def __init__(self):
        self.conn = sqlite3.connect('my_cars.db')
        self.c = self.conn.cursor()
        self.c.execute(create_table_cars)
        self.c.execute(create_table_repairs)

        # temp statement - delete all records
        # with self.conn:
        #     self.c.execute("DELETE FROM repairs")
        #     self.c.execute("DELETE FROM cars")

    def add_car(self, make, model, year, vrn, vin):
        """Adds new car to database.

        Arguments:
        make - car make e.g. Honda
        model - car model e.g. Civic
        year - year of production
        vrn - vehicle registration number
        vin - VIN number

        Returns:
        new Car instance
        """
        with self.conn:
            self.c.execute("INSERT INTO cars VALUES (:make, :model, :year, :vrn, :vin, :sold)", {
                'make': make, 'model': model, 'year': year, 'vrn': vrn, 'vin': vin, 'sold': False})
            return Car(make, model, year, vrn, vin)

    def del_car(self, car):
        """Deletes car from database.

        Arguments:
        car  - car instance

        Returns:
        None
        """

        with self.conn:
            self.c.execute("SELECT ROWID FROM cars WHERE vin=:vin",
                           {'vin': car.vin})
            car_id = self.c.fetchone()
            self.c.execute("DELETE FROM repairs WHERE car=?",
                           (car_id))
            self.c.execute("DELETE FROM cars WHERE vin=:vin", {'vin': car.vin})

    def search_by_vrn(self, vrn):
        """Search car by vehicle registration number.

        Arguments:
        vrn  - vehicle registration number

        Returns:
        search result tuple

        """
        self.c.execute("SELECT * FROM CARS WHERE vrn=:vrn", {'vrn': vrn})
        return self.c.fetchone()

    def show_all_cars(self):
        """Search availale cars.

        Returns:
        search result  - list of tuples

        """
        self.c.execute("SELECT * FROM CARS")
        return self.c.fetchall()

    def set_sold(self, car):
        """Mark car as sold.

        Arguments:
        car  - Car instance

        Returns:
        None
        """

        car.sold = True
        with self.conn:
            self.c.execute("UPDATE cars SET sold=True WHERE vin=:vin", {
                           'vin': car.vin})

    def add_repair(self, car, date, description):
        """Adds repair note.

        Arguments:
        car  - Car instance
        date  - repair date
        description  - repair description

        Returns:
        None
        """
        self.c.execute("SELECT ROWID FROM cars WHERE vin=:vin",
                       {'vin': car.vin})
        car_id = self.c.fetchone()[0]
        with self.conn:
            self.c.execute("INSERT INTO repairs VALUES (:date, :car, :description)", {
                'date': date, 'car': car_id, 'description': description})

    def show_repairs(self, car):
        """Shows car repairs notes.

        Arguments:
        car  - Car instance

        Returns:
        search result  - list of tuples
        """
        self.c.execute("SELECT ROWID FROM cars WHERE vin=:vin",
                       {'vin': car.vin})
        car_id = self.c.fetchone()
        self.c.execute("SELECT * FROM repairs WHERE car=?",
                       (car_id))
        return self.c.fetchall()
