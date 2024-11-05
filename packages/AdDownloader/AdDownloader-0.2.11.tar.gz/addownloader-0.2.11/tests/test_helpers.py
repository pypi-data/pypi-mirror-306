import unittest

# first test the validators
from AdDownloader.helpers import NumberValidator, DateValidator, CountryValidator, ExcelValidator, is_valid_excel_file

class TestNumberValidator(unittest.TestCase):
    def test_valid_number(self):
        """Test for valid number"""
        self.assertTrue(NumberValidator.validate_number(None, '123'))

    def test_invalid_number(self):
        """Test for invalid number"""
        with self.assertRaises(Exception): 
            NumberValidator.validate_number(None, 'abc')


class TestDateValidator(unittest.TestCase):
    def test_valid_date(self):
        """Test for valid date"""
        self.assertTrue(DateValidator.validate_date(None, '2023-12-31'))

    def test_invalid_date(self):
        """Test for invalid date"""
        with self.assertRaises(Exception):
            DateValidator.validate_date(None, '31-12-2023')
            
class TestCountryValidator(unittest.TestCase):
    def test_valid_country(self):
        """Test for valid country"""
        self.assertTrue(CountryValidator.validate_country(None, 'US'))

    def test_invalid_country(self):
        """Test for invalid country"""
        with self.assertRaises(Exception): 
            CountryValidator.validate_country(None, 'XX')


""" from unittest.mock import patch, mock_open
import pandas as pd

class TestExcelValidator(unittest.TestCase):
    @patch('helpers.is_valid_excel_file', return_value=True)
    @patch('helpers.pd.read_excel', return_value=pd.DataFrame({'page_id': [1, 2, 3]}))
    def test_valid_excel(self, mock_read_excel, mock_is_valid_excel_file):
        self.assertTrue(ExcelValidator.validate_excel(None, 'valid_excel.xlsx'))

    @patch('helpers.is_valid_excel_file', return_value=False)
    def test_invalid_excel(self, mock_is_valid_excel_file):
        with self.assertRaises(Exception):
            ExcelValidator.validate_excel(None, 'invalid_excel.xlsx')


class TestIsValidExcelFile(unittest.TestCase):
    @patch('os.path.exists', return_value=True)
    @patch('pandas.read_excel')
    def test_valid_excel_file(self, mock_read_excel, mock_path_exists):
        self.assertTrue(is_valid_excel_file('valid_excel.xlsx'))

    @patch('os.path.exists', return_value=False)
    def test_invalid_excel_file_path(self, mock_path_exists):
        self.assertFalse(is_valid_excel_file('invalid_excel.xlsx'))

    @patch('os.path.exists', return_value=True)
    @patch('pandas.read_excel', side_effect=Exception('Read error'))
    def test_invalid_excel_file_read(self, mock_read_excel, mock_path_exists):
        self.assertFalse(is_valid_excel_file('invalid_excel.xlsx')) """
        
        
# test the flattening functions
from AdDownloader.helpers import flatten_age_country_gender, flatten_demographic_distribution

class TestFlattenAgeCountryGender(unittest.TestCase):
    def test_flatten_age_country_gender(self):
        """Test flatten age_country_gender column"""
        row = [
            {
                "country": "US",
                "age_gender_breakdowns": [
                    {"age_range": "18-24", "male": 10, "female": 15, "unknown": 5},
                    {"age_range": "25-34", "male": 20, "female": 25, "unknown": 10}
                ]
            }
        ]
        target_country = "US"
        expected_output = {
            "US_18-24_male": 10,
            "US_18-24_female": 15,
            "US_18-24_unknown": 5,
            "US_25-34_male": 20,
            "US_25-34_female": 25,
            "US_25-34_unknown": 10
        }
        result = flatten_age_country_gender(row, target_country)
        self.assertEqual(result, expected_output)


class TestFlattenDemographicDistribution(unittest.TestCase):
    def test_flatten_demographic_distribution(self):
        """Test flatten demographic_distribution column"""
        row = [
            {"gender": "male", "age": "18-24", "percentage": "50.0"},
            {"gender": "female", "age": "18-24", "percentage": "50.0"}
        ]
        expected_output = {
            "male_18-24": 50.0,
            "female_18-24": 50.0
        }
        result = flatten_demographic_distribution(row)
        self.assertEqual(result, expected_output)
    

    




if __name__ == '__main__':
    unittest.main(verbosity=2)


