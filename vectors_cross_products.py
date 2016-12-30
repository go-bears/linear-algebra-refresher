from math import sqrt, acos, pi, cos, degrees
from decimal import Decimal, getcontext

# sets precision lenght for decimal objects
getcontext().prec = 7

class Vector(object):
    """Creates template and methods for vector objects """

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
        """prints Vector coordinates as string """

        return 'Vector: {}'.format(self.coordinates)

    def __eq__(self, v):
        """Tests if a vector is equal to another """

        return self.coordinates == v.coordinates

    def plus(self, v):
        """Adds a vector's coordinates with another vector """

        new_coordinates = [x+y for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def minus(self, v):
        """Subtracts a vector's coordinates with another vector """

        new_coordinates = [x-y for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def multiply(self,v):
        multiplied_coordinates = [x*y for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(multiplied_coordinates)

    def times_scalar(self, c):
        """Multiplies vector coordinates by a given scalar unit """

        new_coordinates = [Decimal(x) * c for x in self.coordinates]
        return Vector(new_coordinates)

    def find_magnitude(self):
        """Calcuates magnitude/length of Vector """

        coordinates_squared = [i**2 for i in self.coordinates]
        magnitude = sqrt(sum(coordinates_squared))
        return Decimal(magnitude)

    def find_normalization_vector(self):
        """Returns coordinates of normalized vector unit """

        new_coordinates = []
        try:
            for value in self.coordinates:
                new_coordinates.append(Decimal(value)/self.find_magnitude())
        except ZeroDivisionError:
            raise Exception("Cannot normalize zero vector")

        return Vector(new_coordinates)

    def find_dot_product(self, v):
        """Calcuates dot product of vector and another vector"""

        products = [x*y for x,y in zip(self.coordinates, v.coordinates)]
        return sum(products)

    def find_vectors_angle(self,v, in_degrees=False):
        """Returns an angle between two vectors in radian or degree units"""

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
        """Returns boolean if a vector is orthogonal to another vector"""

        return abs(self.find_dot_product(v)) < tolerance

    def is_parallel_to(self,v):
        """Returns boolean if a vector is parallel to another vector"""

        if self.is_zero() or v.is_zero():
            return True
        elif self.find_vectors_angle(v) == 0:
            return True
        elif self.find_vectors_angle(v) == pi:
            return True
        else:
            return False

    def is_zero(self, tolerance=1e-10):
        """Return boolean for zero precision """

        return self.find_magnitude() < tolerance

    def find_v_parallel_to(self, basis):
        """Returns vector coordinates of vector parallel
        against basis vector"""

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
        """Returns a coordinates of a vector orthogonal
        from basis to vector"""

        try:
            projection = self.find_v_parallel_to(basis)
            return self.minus(projection)

        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception(self.NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG)
            else:
                raise e

    def find_cross_product_of(self, v):
        """Calculates cross product coordinates of 2-d or 3d vectors """
        if self.dimension == 2 and v.dimension == 2:
            y0,y1 = self.coordinates
            z0,z1 = v.coordinates
            return Vector([0.,0., (y0*z1 - y1*z0)])

        if self.dimension == 3 and v.dimension == 3:
            y0, y1, y2 = [Decimal(x) for x in self.coordinates]
            z0, z1, z2 = [Decimal(x) for x in v.coordinates]
            return Vector([(y1*z2) - (y2*z1),
                          -((y0*z2) -(y2*z0)),
                            (y0*z1)- (y1*z0)
                          ])

    def find_parallogram_area_of(self, vector2):
        """Calculates parallelogram area from two vectors """
        cross_product_vector = self.find_cross_product_of(vector2)
        return Decimal(cross_product_vector.find_magnitude())

    def find_triangle_area_of(self, vector2):
        """Calculates right triangle area of parallelogram from two vectors """
        return self.find_parallogram_area_of(vector2) / 2

def main():
    """ quiz for coding cross products"""
    # find cross products of vector v & w
    v = Vector([8.462,7.893,-8.187])
    w = Vector([6.984,-5.975,4.778])
    v_cros_w = v.find_cross_product_of(w)

    # should print coordinates: [-11.205, -97.609, -105.685]
    print v_cros_w

    # find area of a parallelogram spanned by v1 and w1
    v1 = Vector([-8.987,-9.838,5.031])
    w1 = Vector([-4.268,-1.861,-8.866])
    parallelogram_area = v1.find_parallogram_area_of(w1)

    # should print 142.122
    print parallelogram_area

    # find area of a triangle given vectors v2 & w2
    v2 = Vector([1.5,9.547,3.691])
    w2 = Vector([-6.007,0.124,5.772])
    triangle_area = v2.find_triangle_area_of(w2)
    # should print 42.565
    print triangle_area

if __name__ == '__main__':
    main()
