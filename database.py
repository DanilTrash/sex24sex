import pandas as pd


class DataBase:
    URL = 'https://1sex24sex.com/add'
    RUCAPTCHA_APIKEY = '42a3a6c8322f1bec4b5ba84b85fdbe2f'
    GOLOGIN_APIKEY = ('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.e'
                      'yJzdWIiOiI2MTIzOWI2OTkyMGFhMmNmMjBhYTFk'
                      'YjAiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2MTI'
                      '0YTQzZTk3YmI4Y2VmZGI0ODE1YTYifQ.MDc0vL'
                      'O5LM3MsvTbrqSokXbbs3wFmQDL5KihPTZHGiw')
    csv_url = ('https://docs.google.com/spreadsheets/u/1/d/1zaxjdu9ESYy2'
               'MCNuDow0_5PnZpwEsyrdTQ_kk0PMZbw/export?format=csv&id=1za'
               'xjdu9ESYy2MCNuDow0_5PnZpwEsyrdTQ_kk0PMZbw&gid=1432145987')
    df = pd.read_csv(csv_url)
