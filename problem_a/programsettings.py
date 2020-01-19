import argparse

class ProgramSettings:
    '''Stores settings for one run of the program'''

    def __init__(self, target = None, disease = None):
        self.target = target
        self.disease = disease
        self.runTests = False

    @classmethod
    def fromArgs(cls, args):
        parser = argparse.ArgumentParser()
        parser.add_argument('-t', dest='target')
        parser.add_argument('-d', dest='disease')
        parser.add_argument('--test', action='store_true', dest='runTests')
        result = ProgramSettings()
        return parser.parse_args(args, namespace=result)