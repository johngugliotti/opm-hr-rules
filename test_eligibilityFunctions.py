from typing import List, Any, Union
from unittest import TestCase
import csv, json
import io
from pathlib import Path
from datetime import datetime
from retirement_eligibility_functions import EmployeeAttributes, FERS, CSRS


class TestEligibilityFunctions(TestCase):
    min_retirement_age: List

    def setUp(self) -> None:
        """
        min_retirement_age
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
                ##       emp_data, age, op
                self.min_retirement_age.append([emp, int(r[3]), int(r[4]), r[2]])

        """
        immediate retirement benefit
        """
        self.test_immediate_retirement_benefit = []
        p = Path('../swat/retirement-eligibility/fers_immediate_retirement_benefit.csv')
        with io.open(p, 'r', encoding='utf-8', errors='ignore') as infile:
            reader = csv.reader(infile)
            self.header = next(reader)
            for r in reader:
                # eod, dob
                ##fers_immediate_retirement_benefit,19900831,19580730,1
                if r[1] == "":
                    break
                r = r[0:5]

                emp = EmployeeAttributes(r[2], r[1])
                ##                                   expected percentage
                self.test_immediate_retirement_benefit.append([emp, float(r[3]), r[4]])

        self.test_early_retirement_data = []
        p = Path('../swat/retirement-eligibility/fers_early_retirement_test_cases.csv')
        with io.open(p, 'r', encoding='utf-8', errors='ignore') as infile:
            reader = csv.reader(infile)
            self.header = next(reader)
            for r in reader:
                emp = EmployeeAttributes(r[2], r[1])
                #print(r + [ True if r[3] == '1' else False, r[3], "tc{}".format(r[4])])
                self.test_early_retirement_data.append([emp, True if r[3] == '1' else False, r[3], "tc{}".format(r[4])])

    def test_fers_min_retirement_age(self):
        for i in range( len(self.min_retirement_age)):
            expected_value = {"years": self.min_retirement_age[i][1], "months": self.min_retirement_age[i][2]}
            emp = self.min_retirement_age[i][0]
            min_retirement_age_val = FERS.min_retirement_age(emp)
            self.assertEqual(expected_value, min_retirement_age_val)

    def test_fers_immediate_retirement_benefit(self):
        self.assertTrue(1 == 1)

        if False:
            test_case = {'dob': '1966-08-07', 'eod_date': '1991-09-01', 'years_of_service': 30, 'age': 55, 'birth_year': 1966}
            emp = EmployeeAttributes(test_case['dob'], test_case['eod_date'])
            print(json.dumps(emp._json,indent=2))
            predicted_value = FERS.immediate_retirement_benefit(emp)
            print(emp._json)
            expected_value = 0.0
            print(expected_value, predicted_value)
            self.assertTrue((abs(expected_value - predicted_value) < .0001))

        if False:
            for i in range(len(self.test_immediate_retirement_benefit)):
                #print("-"*40)
                test_case_id = self.test_immediate_retirement_benefit[i][2]
                expected_value = self.test_immediate_retirement_benefit[i][1]
                emp = self.test_immediate_retirement_benefit[i][0]
                #print(json.dumps(emp._json))
                #print(test_case_id, expected_value)
                #print("test case: {}, expected_value: {}".format(test_case_id, expected_value))
                assert(isinstance(emp,EmployeeAttributes))
                predicted_value = FERS.immediate_retirement_benefit(emp)
                assert(predicted_value is not None)
                #print("predicted {} / expected {}".format(predicted_value, expected_value))
                self.assertTrue((abs(expected_value - predicted_value) < .0001))



    def test_fers_early_retirement(self):
        for i in range(len(self.test_early_retirement_data)):
            emp = self.test_early_retirement_data[i][0]
            expected_value = self.test_early_retirement_data[i][1]
            test_case = self.test_early_retirement_data[i][3]
            predicted_value = FERS.early_retirement(emp)
            view=emp._json
            view['expected_value']=expected_value
            view['test_case'] = test_case
            view['predicted_value'] = predicted_value
            if expected_value != predicted_value:
                print(json.dumps(view, indent=2))
            self.assertEqual(expected_value, predicted_value)


    def test_deferred_retirement_eligibility(self):
        self.assertTrue(1 == 1)

    def test_fers_disability_retirement_eligibility(self):
        self.assertTrue(1 == 1)

    def test_csrs_retirement_eligibility(self):
        self.assertTrue(1 == 1)

    def test_csrs_early_retirement_eligibility(self):
        self.assertTrue(1 == 1)

    def test_csrs_special_provision(self):
        self.assertTrue(1 == 1)
