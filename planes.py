from decimal import Decimal, getcontext

from vectors_final import Vector

getcontext().prec = 7


class Plane(object):

    NO_NONZERO_ELTS_FOUND_MSG = 'No nonzero elements found'

    def __init__(self, normal_vector=None, constant_term=None):
        self.dimension = 3

        if not normal_vector:
            all_zeros = ['0']*self.dimension
            normal_vector = Vector(all_zeros)
        self.normal_vector = Vector([Decimal(x) for x in normal_vector.coordinates])

        if not constant_term:
            constant_term = Decimal('0')
        self.constant_term = Decimal(constant_term)

        self.set_basepoint()


    def set_basepoint(self):
        try:
            n = self.normal_vector.coordinates
            c = self.constant_term
            basepoint_coords = ['0']*self.dimension

            initial_index = Plane.first_nonzero_index(n)
            initial_coefficient = n[initial_index]

            basepoint_coords[initial_index] = c/initial_coefficient
            self.basepoint = Vector(basepoint_coords)

        except Exception as e:
            if str(e) == Plane.NO_NONZERO_ELTS_FOUND_MSG:
                self.basepoint = None
            else:
                raise e


    def __str__(self):

        num_decimal_places = 3

        def write_coefficient(coefficient, is_initial_term=False):
            coefficient = round(coefficient, num_decimal_places)
            if coefficient % 1 == 0:
                coefficient = int(coefficient)

            output = ''

            if coefficient < 0:
                output += '-'
            if coefficient > 0 and not is_initial_term:
                output += '+'

            if not is_initial_term:
                output += ' '

            if abs(coefficient) != 1:
                output += '{}'.format(abs(coefficient))

            return output

        n = self.normal_vector

        try:
            initial_index = Plane.first_nonzero_index(n)
            terms = [write_coefficient(n[i], is_initial_term=(i==initial_index)) + 'x_{}'.format(i+1)
                     for i in range(self.dimension) if round(n[i], num_decimal_places) != 0]
            output = ' '.join(terms)

        except Exception as e:
            if str(e) == self.NO_NONZERO_ELTS_FOUND_MSG:
                output = '0'
            else:
                raise e

        constant = round(self.constant_term, num_decimal_places)
        if constant % 1 == 0:
            constant = int(constant)
        output += ' = {}'.format(constant)

        return output


    @staticmethod
    def first_nonzero_index(iterable):
        for k, item in enumerate(iterable):
            if not MyDecimal(item).is_near_zero():
                return k
        raise Exception(Plane.NO_NONZERO_ELTS_FOUND_MSG)

    def __eq__(self,plane2):
        """tests if planes are parallel or if same plane """

        # conditional that accomodate a zero vector plane
        if self.normal_vector.is_zero():
            if not plane2.normal_vector.is_zero():
                return False
            else:
                diff = self.constant_term = plane2.constant_term
                return MyDecimal(diff).is_near_zero()
        elif plane2.normal_vector.is_zero():
            return False

        if not self.normal_vector.is_parallel_to(plane2.normal_vector):
            return False

        x_intercept = self.basepoint
        y_intercept = plane2.basepoint
        basepoint_diff = x_intercept.minus(y_intercept)

        n=self.normal_vector
        return basepoint_diff.is_orthogonal_to(basepoint_diff)

    def is_parallel_with(self,plane2):
        """tests is 2 planes are parallel by checking for parallel vectors """

        n1 = self.normal_vector
        n2 = plane2.normal_vector

        return n1.is_parallel_to(n2)

class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps

def main():
    """tests if planes are parallel """
    p1 = Plane(normal_vector=Vector([-0.412,3.806,0.728]), constant_term=-3.46)
    p2 = Plane(normal_vector=Vector([1.03,-9.515,-1.82]), constant_term=8.65)
    print "1) these pairs of planes are parallel?: {}".format(p1.is_parallel_with(p2))
    print '1) these pairs of planes are equal?: {}'.format(p1==p2)


    p3 = Plane(normal_vector=Vector([2.611,5.528,0.283]), constant_term=4.6)
    p4 = Plane(normal_vector=Vector([7.926,8.306,5.342]), constant_term=3.76)
    print "2) these pairs of planes are parallel?: {}".format(p3.is_parallel_with(p4))
    print '2) these pairs of planes are equal?: {}'.format(p3==p4)

    p5 = Plane(normal_vector=Vector([-7.926,8.625,-7.212]), constant_term=7.952)
    p6 = Plane(normal_vector=Vector([-2.642,2.875,-2.404]), constant_term=-2.443)
    print "3) these pairs of planes are parallel?: {}".format(p5.is_parallel_with(p6))
    print '3) these pairs of planes are equal?: {}'.format(p5==p6)

if __name__ == '__main__':
    main()
