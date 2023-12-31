import unittest

from OzonParser import parse_ozon


def parse_test(obj, test_case):
    result = parse_ozon(test_case["url"])
    obj.assertEqual(result["name"], test_case["name"])
    obj.assertEqual(result["brand"], test_case["brand"])
    obj.assertEqual(result["category"], test_case["category"])
    obj.assertTrue(int(result["price"]) > 0)


class FromCategories(unittest.TestCase):

    def test_1(self):
        test_case_1 = {
            "url": "https://www.ozon.ru/product/botinki-stovel-s-dlya-malchikov-1147881853/?advert"
                   "=Q2ctKoJA5eqFqtrUjS6TZ_8Vxoiv-mGU4TOwEAVyg5qCV40mlZsb-3HnSy6W88eEuAGDtZvzUxdbRyV6JuqcaeBr"
                   "-oD6qoSPG6NHuLCpnYfx7BkI0DuCOw9JIzeEQsi7tzxnRTkgocI0uELKR74EBPsxaBSS77re"
                   "-X3h24IL5apMiE8kQYSrNKEKqBxlp2d4hH_Svi9Th7gl0RLuySXd1w0G9HP35"
                   "-qw2ZWOE1YgMmTYpgL1rlwZP93SN8N9Y6kf4k6DaiqjtL4j&avtc=1&avte=2&avts=1698851398",
            "name": "Ботинки STOVEL'S Для мальчиков",
            "brand": "STOVEL'S",
            "category": ['обувь', 'детям', 'мальчикам', 'ботинки']
        }
        parse_test(self, test_case_1)

        test_case_2 = {
            "url": "https://www.ozon.ru/product/dutiki-obba-341872533/?oos_search=false",
            "name": "Дутики Obba",
            'brand': 'Obba',
            'category': ['обувь', 'женщинам']
        }
        parse_test(self, test_case_2)


if __name__ == '__main__':
    unittest.main()
