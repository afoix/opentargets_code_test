import sys
import unittest
from programsettings import ProgramSettings
from query import OverallAssociationScoreQuery

class IntegrationTests(unittest.TestCase):

    def test_case_1(self):
        query = OverallAssociationScoreQuery(ProgramSettings(target='ENSG00000157764'))
        query.run()
        self.assertAlmostEqual(query.min, 0.004)
        self.assertAlmostEqual(query.max, 1.0)
        self.assertAlmostEqual(query.average, 0.3404525)
        self.assertAlmostEqual(query.standard_deviation, 0.339608)

    def test_case_2(self):
        query = OverallAssociationScoreQuery(ProgramSettings(disease='EFO_0002422'))
        query.run()
        self.assertAlmostEqual(query.min, 0.00000202)
        self.assertAlmostEqual(query.max, 1.0)
        self.assertAlmostEqual(query.average, 0.1253773)
        self.assertAlmostEqual(query.standard_deviation, 0.1975769)

    def test_case_3(self):
        query = OverallAssociationScoreQuery(ProgramSettings(disease='EFO_0000616'))
        query.run()
        self.assertAlmostEqual(query.min, 0.000008090)
        self.assertAlmostEqual(query.max, 1.0)
        self.assertAlmostEqual(query.average, 0.4099038)
        self.assertAlmostEqual(query.standard_deviation, 0.3367560)

if __name__ == '__main__':
    settings = ProgramSettings.fromArgs(sys.argv[1:])

    if settings.runTests:
        unittest.main(defaultTest=['IntegrationTests'], argv=sys.argv[1:])

    if settings.target == None and settings.disease == None:
        print ("You must specify either a target (with -t) or a disease (with -d).")
        exit(1)

    query = OverallAssociationScoreQuery(settings)
    query.run()
    print(f'samples: {len(query.values)}; min: {query.min}; max: {query.max}; average: {query.average}; stddev: {query.standard_deviation}')