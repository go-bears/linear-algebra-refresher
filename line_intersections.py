from decimal import Decimal, getcontext

from vectors_final import Vector

getcontext().prec = 7


class Line(object):

    NO_NONZERO_ELTS_FOUND_MSG = 'No nonzero elements found'

    def __init__(self, normal_vector=None, constant_term=None):
        """Line object inherits attributes from Vector object"""
        self.dimension = 2
        self.normal_vector=normal_vector
        constant_term = constant_term

        if not normal_vector:
            all_zeros = ['0']*self.dimension
            normal_vector = Vector(all_zeros)
        self.normal_vector = normal_vector

        if not constant_term:
            constant_term = Decimal('0')
        self.constant_term = Decimal(constant_term)

        self.set_basepoint()


    def set_basepoint(self):
        try:
            n = self.normal_vector.coordinates
            c = self.constant_term
            basepoint_coords = ['0']*self.dimension

            initial_index = Line.first_nonzero_index(n)
            initial_coefficient = n[initial_index]

            basepoint_coords[initial_index] = c/initial_coefficient
            self.basepoint = Vector(basepoint_coords)

        except Exception as e:
            if str(e) == Line.NO_NONZERO_ELTS_FOUND_MSG:
                self.basepoint = None
            else:
                raise e


    def __str__(self):
        """writes line obects in polynomial equation formatted string"""

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

        n = self.normal_vector.coordinates

        try:
            initial_index = Line.first_nonzero_index(n)
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
        raise Exception(Line.NO_NONZERO_ELTS_FOUND_MSG)

    def __eq__(self,line2):
        """tests if lines are parallel or if same line """

        # conditional that accomodate a zero vector line
        if self.normal_vector.is_zero():
            if not line2.normal_vector.is_zero():
                return False
            else:
                diff = self.constant_term = line2.constant_term
                return MyDecimal(diff).is_near_zero()
        elif line2.normal_vector.is_zero():
            return False

        if not self.normal_vector.is_parallel_to(line2.normal_vector):
            return False

        x_intercept = self.basepoint
        y_intercept = line2.basepoint
        basepoint_diff = x_intercept.minus(y_intercept)

        n=self.normal_vector
        return basepoint_diff.is_orthogonal_to(basepoint_diff)


    def intersection_with(self, line2):
        try:
            A,B = self.normal_vector.coordinates
            C,D = line2.normal_vector.coordinates
            k1 = self.constant_term
            k2 = line2.constant_term

            x_numerator = D*k1 - B*k2
            y_numerator = -C*k1 + A*k2
            one_over_denominator = Decimal('1')/(A*D - B*C)

            return Vector([x_numerator,y_numerator]).times_scalar(one_over_denominator)

        except ZeroDivisionError:
            if self == line2:
                return "these are on the same line: {}".format(self)
            else:
                return "intersection is: {}. These are parallel".format(None)


class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps




def main():
    """ tests for functions of intesection lines"""
    # test 1
    line1_vector = Vector([4.046, 2.836])
    line1 = Line(normal_vector=line1_vector, constant_term='1.21')
    # print line1

    line2_vector = Vector([10.115, 7.09])
    line2 = Line(line2_vector, constant_term='3.025')
    # print line2
    print 'intersection 1: ', line1.intersection_with(line2)



    line3_vector = Vector([7.204,3.182])
    line3 = Line(line3_vector, constant_term='8.68')

    line4_vector = Vector([8.172,4.114])
    line4 = Line(line4_vector, constant_term='9.883')
    print "intersection 2: ", line3.intersection_with(line4)

    line5_vector = Vector([1.82,5.562])
    line5 = Line(line4_vector, constant_term='6.744')


    line6_vector = Vector([1.773,8.343])
    line6 = Line(line4_vector, constant_term='9.525')
    print "intersection 3: ", line5.intersection_with(line6)



if __name__ == '__main__':
    main()
