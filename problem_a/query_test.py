import unittest
from math import sqrt
from query import OverallAssociationScoreQuery
from programsettings import ProgramSettings

class TestOverallAssociationScoreQuery(unittest.TestCase):

    def __dummy_settings(self):
        return ProgramSettings(target='ABC123')

    def test_query_url_for_target(self):
        query = OverallAssociationScoreQuery(ProgramSettings(target='ABC123'))
        self.assertEqual(query.baseUrl, 'https://platform-api.opentargets.io/v3/platform/public/association/filter?target=ABC123')

    def test_query_url_for_disease(self):
        query = OverallAssociationScoreQuery(ProgramSettings(disease='ABC123'))
        self.assertEqual(query.baseUrl, 'https://platform-api.opentargets.io/v3/platform/public/association/filter?disease=ABC123')

    def test_cannot_create_query_without_target_or_disease(self):
        with self.assertRaises(Exception):
            OverallAssociationScoreQuery(ProgramSettings())

    def test_get_stats_without_run_fails(self):
        query = OverallAssociationScoreQuery(self.__dummy_settings())
        with self.assertRaises(Exception):
            _ = query.min
        with self.assertRaises(Exception):
            _ = query.max
        with self.assertRaises(Exception):
            _ = query.average
        with self.assertRaises(Exception):
            _ = query.standard_deviation

    def test_min(self):
        query = OverallAssociationScoreQuery(self.__dummy_settings())
        query.values = [1, 2, 3, 4, 5]
        self.assertEqual(query.min, 1)

    def test_max(self):
        query = OverallAssociationScoreQuery(self.__dummy_settings())
        query.values = [1, 2, 3, 4, 5]
        self.assertEqual(query.max, 5)

    def test_average(self):
        query = OverallAssociationScoreQuery(self.__dummy_settings())
        query.values = [1, 2, 3, 4, 5]
        self.assertEqual(query.average, 3)

    def test_standard_deviation(self):
        query = OverallAssociationScoreQuery(self.__dummy_settings())
        query.values = [1, 2, 3, 4, 5]
        self.assertEqual(query.standard_deviation, sqrt(2.5))