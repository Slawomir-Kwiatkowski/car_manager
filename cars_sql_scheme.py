create_table_cars = """CREATE TABLE IF NOT EXISTS cars(
	make TEXT,
	model TEXT,
	year TEXT,
	vrn TEXT,
	vin TEXT,
	sold INTEGER
	)"""

create_table_repairs = """CREATE TABLE IF NOT EXISTS repairs(
	date TEXT,
	car INTEGER,
	description TEXT,
	FOREIGN KEY(car) REFERENCES cars(ROWID)
	)"""