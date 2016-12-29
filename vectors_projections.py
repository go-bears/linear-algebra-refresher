from math import sqrt, acos, pi, cos, degrees
from decimal import Decimal, getcontext

# sets precision lenght for decimal objects
getcontext().prec = 6

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

    def multiply(self,v):
        multiplied_coordinates = [x*y for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(multiplied_coordinates)

    def times_scalar(self, c):
        new_coordinates = [Decimal(x) * c for x in self.coordinates]
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

    def find_v_parallel_to(self, basis):
        try:
            norm_b = basis.find_normalization_vector()
            weight = self.find_dot_product(norm_b)
            return norm_b.times_scalar(weight)

        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception(self.NO_UNIQUE_PARALLEL_COMPONENT_MSG)
            else:
                raise e

    def find_v_orthongonal_to(self,basis):
        try:
            projection = self.find_v_parallel_to(basis)
            return self.minus(projection)

        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception(self.NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG)
            else:
                raise e

def main():
    """ quiz for coding vector projections"""

    # find projected b to vector v
    v=Vector([3.039, 1.879])
    b=Vector([0.825,2.036])
    projected_b = v.find_v_parallel_to(b)

    # print "should print [1.083, 2.672]"
    print projected_b, "\n"

    # find orthogonal vector to vector v2
    v2=Vector([-9.88, -3.264,-8.159])
    b2=Vector([-2.155,-9.353,-9.473])
    v2_orthogonal = v2.find_v_orthongonal_to(b2)

    # should print [-8.350, 3.376, -1.434]
    print v2_orthogonal, "\n"

    print "decomposing a vector:"
    #find vector coordinates of 2 vectors that sum to v5
    v5=Vector([3.009, -6.172, 3.692, -2.51])
    v6=Vector([6.404, -9.144, 2.759, 8.718])

    v5_parallel = v5.find_v_parallel_to(v6)
    v5_orthogonal = v5.find_v_orthongonal_to(v6)

    # should print #v5_a = [1.969, -2.811,0.848,2.680]
    print v5_parallel, "\n"

    # should print #v5_b = [1.040,-3.361,2.844,-5.190]
    print v5_orthogonal





if __name__ == '__main__':
    main()
