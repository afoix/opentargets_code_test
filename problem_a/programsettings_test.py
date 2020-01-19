import unittest
from programsettings import ProgramSettings

class TestProgramSettings(unittest.TestCase):

    def test_default_settings(self):
        settings = ProgramSettings.fromArgs([])
        self.assertIsNone(settings.target)
        self.assertIsNone(settings.disease)
        self.assertFalse(settings.runTests)

    def test_parse_target_arg(self):
        settings = ProgramSettings.fromArgs(['-t', 'abc123'])
        self.assertEqual(settings.target, 'abc123')

    def test_parse_disease_arg(self):
        settings = ProgramSettings.fromArgs(['-d', 'abc123'])
        self.assertEqual(settings.disease, 'abc123')

    def test_parse_runtests_arg(self):
        settings = ProgramSettings.fromArgs(['--test'])
        self.assertTrue(settings.runTests)