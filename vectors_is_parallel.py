from math import sqrt, acos, pi, cos, degrees
from decimal import Decimal, getcontext

getcontext().prec = 30

class Vector(object):
    CANNOT_NORMALIZE_ZERO_VECTOR_MSG = "Cannot normalize the zero vector"

    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(x) for x in coordinates])
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')

    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)

    def __eq__(self, v):
        return self.coordinates == v.coordinates

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
        return Decimal(magnitude)

    def find_normalization_vector(self):
        new_coordinates = []
        try:
            for value in self.coordinates:
                new_coordinates.append(Decimal(value)/self.find_magnitude())
        except ZeroDivisionError:
            raise Exception("Cannot normalize zero vector")

        return Vector(new_coordinates)



    def find_dot_product(self, v):
        products = [x*y for x,y in zip(self.coordinates, v.coordinates)]
        return sum(products)

    def find_vectors_angle(self,v, in_degrees=False):
        try:
            mag1 = self.find_magnitude()
            mag2 = v.find_magnitude()

        except ZeroDivisionError:
            raise Exception("Cannot calculate angle with zero vector")

        ratio = Decimal(self.find_dot_product(v)/Decimal(mag1*mag2))
        if ratio < -1:
            ratio = -1
        elif ratio > 1:
            ratio = 1
        angle_in_radians = Decimal(acos(ratio))

        if in_degrees:
            return degree(angle_in_radians)
        else:
            return angle_in_radians

    def is_orthogonal_to(self,v, tolerance=1e-10):
        return abs(self.find_dot_product(v)) < tolerance

    def is_parallel_to(self,v):
        if self.is_zero() or v.is_zero():
            return True
        elif self.find_vectors_angle(v) == 0:
            return True
        elif self.find_vectors_angle(v) == pi:
            return True
        else:
            return False


    def is_zero(self, tolerance=1e-10):
        return self.find_magnitude() < tolerance



def main():
    """ quiz for is_parallel_to() and is_orthogonal_to()"""
    v=Vector([-7.579, -7.88])
    v2=Vector([22.737, 23.64])
    # should return false
    print v.is_orthogonal_to(v2)
    # should return true
    print v.is_parallel_to(v2)

    v3=Vector([-1.029, 9.97,4.172])
    v4=Vector([-9.231, -6.639,-7.245])
    # should return false
    print v3.is_orthogonal_to(v4)
    # should return true
    print v3.is_parallel_to(v4)

    v5=Vector([-2.328,-7.284,-1.214])
    v6=Vector([-1.821,1.072,-2.94])
    # should return true
    print v5.is_orthogonal_to(v6)
    # should return false
    print v5.is_parallel_to(v6)

    v7=Vector([-2.118,4.827])
    v8=Vector([0,0])
    # should return true
    print v7.is_orthogonal_to(v8)
    # should return false
    print v7.is_parallel_to(v8)

if __name__ == '__main__':
    main()
