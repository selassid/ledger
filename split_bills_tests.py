import unittest
from datetime import date

from split_bills import bill_personal_costs
from split_bills import make_payment
from split_bills import shared_personal_costs
from split_bills import House
from split_bills import Person
from split_bills import Bill
from split_bills import DateRange
from split_bills import Payment
from split_bills import SharedCost


JAN_START = date(2014, 1, 1)
JAN_HALF = date(2014, 1, 16)
JAN_END = date(2014, 1, 31)
JAN_DR = DateRange(start=JAN_START, end_exclusive=JAN_END)
FIRST_HALF_JAN_DR = DateRange(start=JAN_START, end_exclusive=JAN_HALF)
SECOND_HALF_JAN_DR = DateRange(start=JAN_HALF, end_exclusive=JAN_END)


class BillTestCase(unittest.TestCase):
    maxDiff = None

    def test_single_person(self):
        bill = Bill(description=None, for_dates=JAN_DR, amount=100.0, paid_by='Bob')
        person = Person(name='Bob', residencies=(JAN_DR, ))
        house = House(name=None, min_people=1, people=(person, ))

        found_pc = bill_personal_costs(bill, house)
        expected_pc = {'Bob': 0.0}
        self.assertEqual(found_pc, expected_pc)

    def test_two_people(self):
        bill = Bill(description=None, for_dates=JAN_DR, amount=100.0, paid_by='Bob')
        person1 = Person(name='Bob', residencies=(JAN_DR, ))
        person2 = Person(name='Alice', residencies=(JAN_DR, ))
        house = House(name=None, min_people=1, people=(person1, person2))

        found_pc = bill_personal_costs(bill, house)
        expected_pc = {'Bob': -50.0, 'Alice': 50.0}
        self.assertEqual(found_pc, expected_pc)

    def test_half_and_half_person(self):
        bill = Bill(description=None, for_dates=JAN_DR, amount=100.0, paid_by='Bob')
        person1 = Person(name='Bob', residencies=(FIRST_HALF_JAN_DR, ))
        person2 = Person(name='Alice', residencies=(SECOND_HALF_JAN_DR, ))
        house = House(name=None, min_people=1, people=(person1, person2))

        found_pc = bill_personal_costs(bill, house)
        expected_pc = {'Bob': -50.0, 'Alice': 50.0}
        self.assertEqual(found_pc, expected_pc)

    def test_one_and_half_person(self):
        bill = Bill(description=None, for_dates=JAN_DR, amount=100.0, paid_by='Bob')
        person1 = Person(name='Bob', residencies=(JAN_DR, ))
        person2 = Person(name='Alice', residencies=(FIRST_HALF_JAN_DR, ))
        house = House(name=None, min_people=1, people=(person1, person2))

        found_pc = bill_personal_costs(bill, house)
        expected_pc = {'Bob': -25.0, 'Alice': 25.0}
        self.assertEqual(found_pc, expected_pc)


class SharedCostTestCase(unittest.TestCase):
    maxDiff = None

    def test_shared(self):
        shared = SharedCost(description=None, paid_by='Bob', on_date=JAN_START, shared_amongst=frozenset(('Bob', 'Alice')), amount=100.0)

        found_pc = shared_personal_costs(shared)
        expected_pc = {'Bob': 50.0, 'Alice': -50.0}
        self.assertEqual(found_pc, expected_pc)


class PaymentsTestCase(unittest.TestCase):
    maxDiff = None

    def test_payment(self):
        payment = Payment(payer='Bob', to='Alice', amount=100.0, on_date=JAN_START)

        found_pc = make_payment(payment)
        expected_pc = {'Bob': 100.0, 'Alice': -100.0}
        self.assertEqual(found_pc, expected_pc)


if __name__ == '__main__':
    unittest.main()
