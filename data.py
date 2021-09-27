import pandas as pd
import numpy as np
from collections.abc import Iterator


class Data(Iterator):
    URL = 'https://1sex24sex.com/add'
    RUCAPTCHA_APIKEY = '42a3a6c8322f1bec4b5ba84b85fdbe2f'
    GOLOGIN_APIKEY = (
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2MTQwODg1MDM2MzkxOGU1YjdlNWFiNWIiL'
        'CJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2MTQwODhiODY4Y2E1Njc5NGEwZGNjNWEifQ.eVVNLIeuvRJ-Z'
        'PotsEuZtNAzNd39SB9HdBwa1CqqHdo'
    )
    csv_url = ('https://docs.google.com/spreadsheets/u/1/d/1zaxjdu9ESYy2'
               'MCNuDow0_5PnZpwEsyrdTQ_kk0PMZbw/export?format=csv&id=1za'
               'xjdu9ESYy2MCNuDow0_5PnZpwEsyrdTQ_kk0PMZbw&gid=1432145987')
    dataframe = pd.read_csv(csv_url, dtype={'number': str, 'region': str})

    def __init__(self, argument, position=0, threads=1) -> None:
        if threads > 1:
            self._collection = np.array_split(self.dataframe[argument].dropna().tolist(), threads)[position]
        else:
            self._collection = self.dataframe[argument].dropna().tolist()
        self.position = position

    def __next__(self) -> str:
        try:
            value = self._collection[self.position]
            self.position += 1
            return value
        except IndexError:
            raise StopIteration
