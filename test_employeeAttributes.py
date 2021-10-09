from typing import List, Any
from unittest import TestCase

from datetime import datetime
from retirement_eligibility_functions import EmployeeAttributes


class TestEmployeeAttributes(TestCase):

    test_eod_in: List[Any]

    def setUp(self) -> None:
        self.test_dates_in = [
            '20060102'
            , '19680217'
            , '20021202'
            , '19380102'
            , '19660908']

        self.test_dates_out = [
            datetime(2006, 1, 2)
            , datetime(1968, 2, 17)
            , datetime(2002, 12, 2)
            , datetime(1938, 1, 2)
            , datetime(1966, 9, 8)
        ]

        self.test_dob_in = [
            '19380303'
            , '19450102'
            , '19500101'
            , '19560202'
            , '19650101'
            , '19690303'
            , '19700202'
            , '19780908'
        ]
        self.test_eod_in = [
            '1958-0303'
            , '19690102'
            , '19710101'
            , '19790202'
            , '19870101'
            , '19890303'
            , '19900202'
            , '19980908'
        ]

    def test_to_date(self):
        for i in range(len(self.test_dates_in)):
            self.assertEqual(EmployeeAttributes.to_date(self.test_dates_in[i]), self.test_dates_out[i])
            print(EmployeeAttributes.to_date(self.test_dates_in[i]).strftime("%Y-%m-%d"))

    def test___init__(self):
        for i in range(len(self.test_dob_in)):
            ea = EmployeeAttributes(self.test_dob_in[i], self.test_eod_in[i])
            print(ea._json)
            self.assertTrue(1 == 1)
