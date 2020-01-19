import requests
import statistics

DEFAULT_ENDPOINT_URI = "https://platform-api.opentargets.io/v3/platform/public/association/filter"
DEFAULT_PAGE_SIZE = 1000

class OverallAssociationScoreQuery:
    '''Queries the REST API for data and stores the result'''

    def __init__(self, settings, endpoint = DEFAULT_ENDPOINT_URI, pageSize = DEFAULT_PAGE_SIZE):

        if settings.target is not None:
            self.baseUrl = f'{endpoint}?target={settings.target}'
        elif settings.disease is not None:
            self.baseUrl = f'{endpoint}?disease={settings.disease}'
        else:
            raise Exception("Neither target nor disease were specified")

        self.pageSize = pageSize
        self.values = []

    def run(self):

        if len(self.values) > 0:
            raise Exception("Already ran!")

        baseUrl = f'{self.baseUrl}&size={self.pageSize}'
        pageUrl = f'{baseUrl}'
        while True:
            jsonObj = requests.get(pageUrl).json()
            for entry in jsonObj["data"]:
                self.values.append(entry["association_score"]["overall"])

            if not 'next' in jsonObj:
                return

            pageUrl = baseUrl
            for nextVal in jsonObj["next"]:
                pageUrl = f'{pageUrl}&next={nextVal}'

    def __check_has_run(self):
        if len(self.values) == 0:
            raise Exception("You must run() this query first")

    @property
    def min(self):
        self.__check_has_run()
        return min(self.values)

    @property
    def max(self):
        self.__check_has_run()
        return max(self.values)

    @property
    def average(self):
        self.__check_has_run()
        return statistics.mean(self.values)

    @property
    def standard_deviation(self):
        self.__check_has_run()
        return statistics.stdev(self.values)