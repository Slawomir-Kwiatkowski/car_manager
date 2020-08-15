class Car():
    """Represents a sample car.

    Arguments:
    make - car make e.g. Honda
    model - car model e.g. Civic
    year - year of production
    vrn - vehicle registration number
    vin - VIN number
    sold - if car is still our property

    """

    def __init__(self, make, model, year, vrn, vin, sold=False):
        self.repairs = []
        self.make = make

        self.model = model
        self.year = year
        self.vrn = vrn
        self.vin = vin
        self.sold = sold

    @classmethod
    def from_list(cls, list):
        make, model, year, vrn, vin, sold = list
        return cls(make, model, year, vrn, vin, sold)
