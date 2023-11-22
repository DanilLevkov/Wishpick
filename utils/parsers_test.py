import unittest

import parsers

price_cases = [
    {"input": "от 1000 до 5000",
     "expected": {"from": 1000,
                  "to": 5000}
     },
    {"input": "от ничего до много",
     "expected": None
     },
    {"input": "kfvd dmnv dfv dv dbf dnb fv",
     "expected": None
     },
    {"input": "",
     "expected": None
     },
    {"input": None,
     "expected": None
     },
    {"input": "от 1 до 5",
     "expected": {"from": 1000,
                  "to": 5000}
     },
    {"input": "от 100",
     "expected": {"from": 100,
                  "to": None}
     },
    {"input": "до 9000000",
     "expected": {"from": None,
                  "to": 9000000}
     },
    {"input": "   от    1000    до    5000    ",
     "expected": {"from": 1000,
                  "to": 5000}
     },
    {"input": " текст вокруг от    1000  текст вокруг  до    5000  текст вокруг  ",
     "expected": {"from": 1000,
                  "to": 5000}
     },
    {"input": "до 8000 и от 500",
     "expected": {"from": 500,
                  "to": 8000}
     },
    {"input": "от1000 до5000",
     "expected": {"from": 1000,
                  "to": 5000}
     },
    {"input": "от 500 руб. до 500 руб.",
     "expected": {"from": 500,
                  "to": 500}
     },
    {"input": "от -500 руб. до 1000 руб.",
     "expected": {"from": 0,
                  "to": 1000}
     },
    {"input": "от 1.5 руб. до 1000 руб.",
     "expected": {"from": None,
                  "to": 1000}
     },
]


class ParserTestCase(unittest.TestCase):
    def test_get_price_range(self):
        for case in price_cases:
            result = parsers.get_price_range(case["input"])
            expected = case["expected"]
            if not result:
                self.assertTrue(expected is None, msg=case["input"])
            else:
                self.assertDictEqual(result, expected, msg=case["input"])


if __name__ == '__main__':
    unittest.main()
