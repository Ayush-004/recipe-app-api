
'''
Sample tests
'''

from django.test import SimpleTestCase

from app import calc

class CalcTests(SimpleTestCase):
    ''' Test the calc module.'''
    
    def test_add_numbers(self):
        res = calc.add(5,6)
        # print(res)
        self.assertEqual(res,11)

    def test_substract_numbers(self):
        '''Test subtracting number'''
        res = calc.substract(10,5)
        self.assertEqual(res,5)

