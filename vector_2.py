from math import sqrt

class Vector(object):
    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple(coordinates)
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')

    def plus(self, v):
        new_coordinates = [x+y for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def minus(self, v):
        new_coordinates = [x-y for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def times_scalar(self, c):
        new_coordinates = [c*x for x in self.coordinates]
        return Vector(new_coordinates)

    def find_magnitude(self):
        coordinates_squared = [i**2 for i in self.coordinates]
        magnitude = sqrt(sum(coordinates_squared))
        return magnitude

    def find_normalization_vector(self):
        try:
            magnitude = self.find_magnitude()
            normalization = self.times_scalar(1/magnitude)
            return normalization

        except ZeroDivisionError:
            raise Exception("Cannot normalize the zero vector")

    def find_dot_product(self, v):
        products = [x*y for x,y in zip(self.coordinates, v.coordinates)]
        return sum(products)

    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)


    def __eq__(self, v):
        return self.coordinates == v.coordinates
