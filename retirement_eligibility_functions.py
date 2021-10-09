import math
from datetime import datetime, timedelta
import re


class ServiceClasses:
    """
    for air traffic controllers or law enforcement and firefighter personnel, nuclear materials courier
    , Supreme Court Police and Capitol Police.
    """

    def __init__(self):
        self.service_classes = {
            "air traffic controller"
            , "law enforcement"
            , "Supreme Court Police"
            , "Capitol Police"
        }


class EmployeeAttributes:
    birth_year: int
    eod_date: datetime
    dob: datetime

    @staticmethod
    def to_date(dt_string: str) -> datetime:
        if re.search('[\d]{4}[\-]*[\d]{1,2}[\-]*[\d]{1,2}', dt_string):
            dt_string = re.sub("[\-\/]", "", dt_string)
            dt = datetime.strptime(dt_string, '%Y%m%d')
            return dt
        else:
            raise Exception('invalid date format')

    def __init__(self, dob: str = None, eod_date: str = None, appointment_type: str = None,
                 services_classes=[]):
        """

        :type eod_date: datetime
        :type dob: datetime

        """
        days_in_months = [31, 28.25, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        self.dob = self.to_date(dob)

        self.eod_date = self.to_date(eod_date)
        self.retirement_system = FERS if self.eod_date >= datetime(1987, 1, 1) else CSRS
        self.appointment_type = appointment_type

        self.years_of_service = math.floor(((datetime.now() - self.eod_date).days / 365.25))
        self.age = math.floor(((datetime.now() - self.dob).days / 365.25))
        self.age_years = math.floor(((datetime.now() - self.dob).days / 365.25))
        self.age_months = math.floor(
            (((datetime.now() - self.dob).days / 365.25) - math.floor((datetime.now() - self.dob).days / 365.25)) * 12)
        self.birth_year = self.dob.year

        self.minimum_retirement_age = FERS.min_retirement_age(self)
        months = self.minimum_retirement_age.get('months')
        min_retirement_days = sum(days_in_months[0: months])
        min_retirement_days += int(math.floor(self.minimum_retirement_age.get('years') * 365.25))
        self.meets_minimum_age_criteria = (self.age >= self.minimum_retirement_age.get('years')) \
                                          and (self.age_months >= self.minimum_retirement_age.get('months'))

    @property
    def _json(self):
        return {
            "dob": self.dob.strftime("%Y-%m-%d"),
            "eod_date": self.eod_date.strftime("%Y-%m-%d"),
            "years_of_service": self.years_of_service,
            "age": self.age,
            "birth_year": self.birth_year,
            "minimum_retirement_age": self.minimum_retirement_age,
            "meets_minimum_age_criteria": self.meets_minimum_age_criteria
        }


## FERS
class FERS:
    """
        https://www.opm.gov/retirement-services/fers-information/eligibility
    """
    @classmethod
    def __str__(cls) -> str:
        return 'FERS'

    @staticmethod
    def min_retirement_age(emp: EmployeeAttributes = None) -> dict:
        if emp.birth_year <= 1947:
            return {"years": 55, "months": 0}
        elif emp.birth_year == 1948:
            return {"years": 55, "months": 2}
        elif emp.birth_year == 1949:
            return {"years": 55, "months": 4}
        elif emp.birth_year == 1950:
            return {"years": 55, "months": 6}
        elif emp.birth_year == 1951:
            return {"years": 55, "months": 8}
        elif emp.birth_year == 1952:
            return {"years": 55, "months": 10}
        elif emp.birth_year in range(1953, 1964 + 1):
            return {"years": 56, "months": 0}
        elif emp.birth_year == 1965:
            return {"years": 56, "months": 2}
        elif emp.birth_year == 1966:
            return {"years": 56, "months": 4}
        elif emp.birth_year == 1967:
            return {"years": 56, "months": 6}
        elif emp.birth_year == 1968:
            return {"years": 56, "months": 8}
        elif emp.birth_year == 1969:
            return {"years": 56, "months": 10}
        else:
            # 1970 and after
            return {"years": 57, "months": 0}

    @staticmethod
    def early_retirement(emp: EmployeeAttributes) -> bool:
        """
        Early Retirement

        The early retirement benefit is available in certain involuntary separation cases
        and in cases of voluntary separations during a major reorganization or reduction in force.

            Eligibility Information
            Age	    Years of Service
            50	    20
            Any Age	25
        """
        print(emp.years_of_service, emp.age, "\n-----------------")
        if emp.years_of_service < 20 or emp.age < 36:
            # minimum legal employment age plus 20 years
            print("fail case 1")
            return False
        if emp.years_of_service >= 20 and emp.age >= 50:
            # age 50 and older with 20 or more years of service
            print("case 2 age 50 and older with 20 or more years of service")
            return True
        elif emp.years_of_service >= 25 and emp.age >= 25 + 16:
            # any age with 25 or more years of service
            print("case 3: any age with 25 or more years of service")
            return True
        else:
            print("fall out")
            return False

    @staticmethod
    def deferred_retirement_eligibility(emp: EmployeeAttributes) -> bool:
        """
        Deferred Retirement

        If you leave Federal service before you meet the age and service requirements
        for an immediate retirement benefit, you may be eligible for deferred retirement benefits.
        To be eligible, you must have completed at least 5 years of creditable civilian service.
        You may receive benefits when you reach one of the following ages:

            Eligibility Information
            Age	Years of Service
            62	5
            MRA	30
            MRA	10
        """
        return (emp.age >= 62 and emp.years_of_service >= 5) \
               or (emp.meets_minimum_age_criteria and emp.years_of_service >= 30) \
               or (emp.meets_minimum_age_criteria and emp.years_of_service >= 10)
        return emp.years_of_service >= 5

    @staticmethod
    def disability_retirement_eligibility(emp: EmployeeAttributes) -> bool:
        """
            Age / Years of Service
            Any Age	/ 18 months
            Special Requirements : You must have become disabled, while employed in a position subject to FERS,
            because of a disease or injury, for useful and efficient service in your current position.
            The disability must be expected to last at least one year. Your agency must certify that it is unable
            to accommodate your disabling medical condition in your present position and
            that it has considered you for any vacant position in the same agency at the same grade/pay level
            , within the same commuting area, for which you are qualified for reassignment.
        :param emp:
        :return: boolean True if employee meets qualifications and false otherwise
        """
        return (datetime.now() - emp.eod_date).days >= (1.5 * 365.25)  # 18 months


    @staticmethod
    def immediate_retirement_benefit(emp: EmployeeAttributes) -> float:
        """
            If you retire at the MRA with at least 10, but less than 30 years of service,
            your benefit will be reduced by 5 percent a year for each year you are under 62,
            unless you have 20 years of service and your benefit starts
            when you reach age 60 or later.

            Age	Years of Service
            62	5
            60	20
            MRA	30
            MRA	10
            MRA = minimum retirement age
        """

        if emp.meets_minimum_age_criteria:
            if 10 <= emp.years_of_service < 30:
                adjusted_retirement_benefit = 1.0 - ((62.0 - float(emp.age)) * 0.05)
                print("condition 1.A: age -> {} , reduction {}".format(emp.age, (62.0 - float(emp.age)) * 0.05))
                return min(adjusted_retirement_benefit, 1.0)
            elif emp.years_of_service >= 30:
                print("condition 1.B: age -> {}".format(emp.age))
                return 1.0
            else:
                return 0.0
        elif (emp.years_of_service >= 20 and emp.age >= 60) or (emp.years_of_service >= 5 and emp.age >= 62):
            print("condition TWO")
            return 1.0
        else:
            print("condition THREE")
            return 0.0


class CSRS:
    """
    https://www.opm.gov/retirement-services/csrs-information/

    There are five categories of benefits under the Civil Service Retirement System (CSRS).
    Eligibility is based on your age and the number of years of creditable service and any other special requirements.
    In addition, you must have served in a position subject to CSRS coverage for one of the last two years
        before your retirement.
    If you meet one of the following sets of requirements, you may be eligible for an immediate retirement benefit.
    An immediate annuity is one that begins within 30 days after your separation.

    Optional
    If you leave Federal service before you meet the age and service requirements for an immediate retirement benefit,
        you may be eligible for deferred retirement benefits.
    To be eligible, you must have at least 5 years of creditable civilian service and be age 62.
    """

    """
    Age	Years of Service
    62	5
    60	20
    55	30
    """

    @classmethod
    def __str__(cls) -> str:
        return 'CSRS'

    @staticmethod
    def retirement_eligibility(emp: EmployeeAttributes):
        return (emp.years_of_service >= 5 and emp.age >= 62) \
               or (emp.years_of_service >= 25 and emp.age >= 60) \
               or (emp.years_of_service >= 30 and emp.age >= 55)

    """
    Special/Early Optional
    Special/Early Optional Requirements: 
    Your agency must be undergoing a major reorganization
    , reduction-in-force, or transfer of function determined by the Office of Personnel Management. 
    Your annuity is reduced if you are under age 55.
    
    Age	Years of Service
    50	20
    Any Age	25
    """

    def early_retirement_eligibility(emp: EmployeeAttributes) -> bool:
        """Special Provision Retirement
            Special Requirements: You must retire under special provisions for:
                air traffic controllers
                law enforcement and firefighter personnel
                nuclear materials courier
                supreme Court Police
                Capitol Police

            Age	Years of Service
            50	20
            Any Age *	25
            * ONLY air traffic controllers can retire at any age with 25 years of service as an air traffic controller.
        """
        return (emp.years_of_service >= 20 and emp.age >= 50) or \
               (emp.years_of_service >= 25 and emp.age >= (16 + 25))

    @staticmethod
    def discontinued_service_retirement(emp: EmployeeAttributes) -> bool:
        """
        Discontinued Service
        Age	Years of Service
        50	20
        Any Age	25
        Special Requirements: Your separation is involuntary and not a removal for misconduct or delinquency.
        """
        return (emp.years_of_service >= 20 and emp.age >= 50) or \
               (emp.years_of_service >= 25 and emp.age >= (16 + 25))

    @staticmethod
    def special_provision(emp: EmployeeAttributes) -> bool:
        return (emp.years_of_service >= 20 and emp.age >= 50) \
               or (emp.years_of_service >= 25 and emp.age >= (16 + 25))

    def disability_retirement(emp: EmployeeAttributes):
        """
        Disability
        Age	Years of Service
        Any Age	5
        Special Requirements: You must be disabled for useful and efficient service in your current position and any other
            vacant position at the same grade or pay level within your commuting area and current agency for which you
            are qualified. You must have been disabled prior to retirement and the disability should be expected to
            last for more than one year.
        """
        return emp.years_of_service >= 5 and emp.age >= (16 + 5)  ## min employment age plus five years
