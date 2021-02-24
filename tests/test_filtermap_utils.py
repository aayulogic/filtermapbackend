from unittest import TestCase

from filter_map.utils import get_applicable_filters, inverse_mapping


class GetApplicableFiltersTestCase(TestCase):
    """
    Test Cases for get_applicable_filters util.

    To append test cases in test cases variable in following format,
    {
        "filter_map": {},
        "query_params": {},
        "expected_output": {},
        "case": ""
    }

    """

    test_cases = [
        {
            "filter_map": {
                "display_name": "field_name"
            },
            "query_params": {
                "display_name": "value"
            },
            "expected_output": {
                "field_name": "value"
            },
            "case": "Default Case"
        },
        {
            "filter_map": {
                "display_name": "field_name"
            },
            "query_params": {
                "display_name": ""
            },
            "expected_output": {
            },
            "case": "Blank Case"
        }
    ]

    def test_get_applicable_filters(self):
        for test_case in self.test_cases:
            output = get_applicable_filters(test_case['query_params'], test_case.get('filter_map'))
            self.assertEqual(
                output,
                test_case['expected_output'],
                f"Failed case {test_case['case']}"
            )


class InverseMappingTestCase(TestCase):
    def test_inverse_mapping(self):
        input_data = {
            "a": "b",
            "c": "d",
            "e": "f"
        }
        expected_output = {
            "b": "a",
            "d": "c",
            "f": "e"
        }
        output = inverse_mapping(input_data)
        self.assertEqual(output, expected_output)
