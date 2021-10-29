from typing import List, Any, Union
from unittest import TestCase
import csv, json
import io
from datetime import datetime, timedelta
from pathlib import Path
from datetime import datetime
from retirement_eligibility_functions import EmployeeAttributes, FERS, CSRS


class TestEligibilityFunctions(TestCase):
    min_retirement_age: List

    def setUp(self) -> None:
        """
        LOAD min_retirement_age
        """
        self.min_retirement_age = []
        p = Path('../swat/retirement-eligibility/fers_min_retirement_age.csv')
        with io.open(p, 'r', encoding='utf-8', errors='ignore') as infile:
            reader = csv.reader(infile)
            self.header = next(reader)
            for r in reader:
                if r[1] == "":
                    break
                r = r[0:5]
                emp = EmployeeAttributes(r[1], '19700101')
                self.min_retirement_age.append([emp, int(r[3]), int(r[4]), r[2]])

        """
        LOAD immediate retirement benefit
        """
        self.test_immediate_retirement_benefit = []
        p = Path('../swat/retirement-eligibility/fers_immediate_retirement_benefit.csv')
        with io.open(p, 'r', encoding='utf-8', errors='ignore') as infile:
            reader = csv.reader(infile)
            self.header = next(reader)
            for r in reader:
                if r[1] == "":
                    break
                r = r[0:5]
                emp = EmployeeAttributes(r[2], r[1])
                self.test_immediate_retirement_benefit.append([emp, float(r[3]), r[4]])

        """
        LOAD early retirement
        """
        self.test_early_retirement_data = []
        p = Path('../swat/retirement-eligibility/fers_early_retirement_test_cases.csv')
        with io.open(p, 'r', encoding='utf-8', errors='ignore') as infile:
            reader = csv.reader(infile)
            self.header = next(reader)
            for r in reader:
                emp = EmployeeAttributes(r[2], r[1])
                self.test_early_retirement_data.append([emp, True if r[3] == '1' else False, r[3], "tc{}".format(r[4])])
        """
        LOAD deferred retirement eligibility
        """
        self.fers_deferred_retirement_eligibility_cases = []
        p = Path('../swat/retirement-eligibility/fers_deferred_retirement_eligibility_cases.csv')
        with io.open(p, 'r', encoding='utf-8', errors='ignore') as infile:
            reader = csv.reader(infile)
            self.header = next(reader)

            for r in reader:
                emp = EmployeeAttributes(r[1], r[0])
                res = int(r[2])
                test_case = r[3]
                self.fers_deferred_retirement_eligibility_cases.append([emp, res, test_case])
        """
        LOAD disability retirement eligibility
        """
        # we will manufacture this data randomly since the only criteria is years of service
        self.fers_disability_retirement_eligibility_cases = []
        import random
        ages = [20, 30, 40, 50, 57, 60, 62, 63, 70]
        tos = [int(1.4 * 365.25), int(1.5 * 366), int(1.6 * 365.25)]
        expected_values = [False, True, True]
        for i in range(len(ages)):
            dob = datetime.now() - timedelta(days=int(ages[i] * 365.25))
            for j in range(len(expected_values)):
                scrddate = datetime.now() - timedelta(days=tos[j])
                emp = EmployeeAttributes(dob.strftime('%Y%m%d'), scrddate.strftime('%Y%m%d'))
                trec=[emp, expected_values[j], 'tc{}'.format(i+1)]
                self.fers_disability_retirement_eligibility_cases.append(trec)

        #
        # p = Path('../swat/retirement-eligibility/fers_disability_retirement_eligibility_cases.csv')
        # with io.open(p, 'r', encoding='utf-8', errors='ignore') as infile:
        #     reader = csv.reader(infile)
        #     self.header = next(reader)
        #     for r in reader:
        #         self.fers_disability_retirement_eligibility_cases.append([])
        #
        #      $$$     $$$
        #     $   $   $   $
        #     $   $    $
        #     $         $
        #     $   $      $
        #     $   $   $   $
        #      $$$     $$$
        #
        # CSRS
        self.csrs_retirement_eligible_cases = []
        p = Path('../swat/retirement-eligibility/csrs_retirement_eligibility_cases.csv')
        with io.open(p, 'r', encoding='utf-8', errors='ignore') as infile:
            reader = csv.reader(infile)
            self.header = next(reader)
            for r in reader:
                emp = EmployeeAttributes(r[1], r[0])
                expected_value = True if int(r[2]) == 1 else 0
                test_case = r[3]
                self.csrs_retirement_eligible_cases.append([emp, expected_value, test_case])

        self.csrs_early_retirement_eligibility_cases = []
        p = Path('../swat/retirement-eligibility/csrs_early_retirement_eligibility_cases.csv')
        with io.open(p, 'r', encoding='utf-8', errors='ignore') as infile:
            reader = csv.reader(infile)
            self.header = next(reader)
            for r in reader:
                emp = EmployeeAttributes(r[1], r[0])
                expected_value = True if int(r[2]) == 1 else False
                test_case = r[3]
                self.csrs_early_retirement_eligibility_cases.append([emp, expected_value, test_case])

        self.csrs_special_provision_cases = []
        p = Path('../swat/retirement-eligibility/csrs_special_provision_cases.csv')
        with io.open(p, 'r', encoding='utf-8', errors='ignore') as infile:
            reader = csv.reader(infile)
            self.header = next(reader)
            for r in reader:
                self.csrs_special_provision_cases.append([])

        self.discontinued_service_retirement_cases = []
        p = Path('../swat/retirement-eligibility/discontinued_service_retirement_cases.csv')
        with io.open(p, 'r', encoding='utf-8', errors='ignore') as infile:
            reader = csv.reader(infile)
            self.header = next(reader)
            for r in reader:
                self.discontinued_service_retirement_cases.append([])

    def test_fers_min_retirement_age(self):
        for i in range(len(self.min_retirement_age)):
            expected_value = {"years": self.min_retirement_age[i][1], "months": self.min_retirement_age[i][2]}
            emp = self.min_retirement_age[i][0]
            min_retirement_age_val = FERS.min_retirement_age(emp)
            self.assertEqual(expected_value, min_retirement_age_val)

    def test_fers_immediate_retirement_benefit(self):
        if False:
            test_case = {'dob': '1966-08-07', 'scrd': '1991-09-01', 'years_of_service': 30, 'age': 55,
                         'birth_year': 1966}
            emp = EmployeeAttributes(test_case['dob'], test_case['scrd'])
            predicted_value = FERS.immediate_retirement_benefit(emp)
            expected_value = 0.0
            self.assertTrue((abs(expected_value - predicted_value) < .0001))

        if True:
            for i in range(len(self.test_immediate_retirement_benefit)):
                test_case_id = self.test_immediate_retirement_benefit[i][2]
                expected_value = self.test_immediate_retirement_benefit[i][1]
                emp = self.test_immediate_retirement_benefit[i][0]
                assert (isinstance(emp, EmployeeAttributes))
                predicted_value = FERS.immediate_retirement_benefit(emp)
                assert (predicted_value is not None)
                self.assertTrue((abs(expected_value - predicted_value) < .0001))

    def test_fers_early_retirement(self):
        for i in range(len(self.test_early_retirement_data)):
            emp = self.test_early_retirement_data[i][0]
            expected_value = self.test_early_retirement_data[i][1]
            test_case = self.test_early_retirement_data[i][3]
            predicted_value = FERS.early_retirement(emp)
            self.assertEqual(expected_value, predicted_value)

    def test_fers_deferred_retirement_eligibility(self):
        # self.assertTrue(1 == 1)
        # result	test_case
        for r in self.fers_deferred_retirement_eligibility_cases:
            emp = r[0]
            predicted_value = FERS.deferred_retirement_eligibility(emp)
            expected_value = True if r[1] == 1 else False
            test_case = r[2]
            self.assertEqual(expected_value, predicted_value)

    def test_fers_disability_retirement_eligibility(self):
        for r in self.fers_disability_retirement_eligibility_cases:
            emp = r[0]
            expected_value = r[1]
            test_case = r[2]
            predicted_value = FERS.disability_retirement_eligibility(emp)
            if expected_value != predicted_value: print(test_case)
            self.assertEqual(expected_value, predicted_value)

    #CSRS

    def test_csrs_retirement_eligible(self):
        for r in self.csrs_retirement_eligible_cases:
            emp = r[0]
            expected_value = r[1]
            test_case = r[2]
            predicted_value = CSRS.retirement_eligible(emp)
            print(emp._json)
            print(test_case, expected_value, predicted_value)
            self.assertEqual(expected_value, predicted_value)

    def test_csrs_early_retirement_eligibility(self):
        for r in self.csrs_early_retirement_eligibility_cases:
            emp = r[0]
            expected_value = r[1]
            test_case = r[2]
            predicted_value = CSRS.early_retirement_eligibility(emp)
            self.assertEqual(expected_value, predicted_value)
    """
    include additional information in the employeee object which is to be derived from NOA codes:
    - onboarding NOA code or other contextual information that indicates the type of hire
    - this may only apply as a distinctive function for FAA (air traffic controllers who can retire at any age with 25 y.o.s.
    """
    def test_csrs_special_provision(self):
        for r in self.csrs_early_retirement_eligibility_cases:
            emp = r[0]
            expected_value = r[1]
            test_case = r[2]
            predicted_value = CSRS.early_retirement_eligibility(emp)
            self.assertEqual(expected_value, predicted_value)

    """
    Special Requirements: Your separation is involuntary and not a removal for misconduct or delinquency.
        NOA code or additional exit context may be a factor here
        This will require the addition of more information to the employee object
    """
    def test_discontinued_service_retirement(self):
        for r in self.csrs_early_retirement_eligibility_cases:
            emp = r[0]
            expected_value = r[1]
            test_case = r[2]
            predicted_value = CSRS.early_retirement_eligibility(emp)
            self.assertEqual(expected_value, predicted_value)

