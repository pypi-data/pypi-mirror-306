# Importing Necessary Libraries
import pandas as pd
import requests
from datetime import datetime, timedelta
from pytz import timezone
import pickle
import pathlib
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from io import StringIO
import dateutil.parser as parser

# Company symbol finder
class ValueError(Exception):
    pass

class Stock():
    def __init__(self, identifier:str):
        """For scrapping stock historical informations.

        Args:
            stock_name (str): Listed Company/Stock/Index
        """
        self.identifier       = identifier
        self.max_retries      = 10
        self.backoff_factor   = 0.5
        self.status_forcelist = [500, 502, 503, 504]
        self.head             = {
                                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                              "Chrome/87.0.4280.88 Safari/537.36 "}
        self.date_format      = "%d-%b-%Y"
        self.HERE             = pathlib.Path(__file__).parent.resolve()
        self.retry            = Retry(total             = self.max_retries,
                                      backoff_factor    = self.backoff_factor,
                                      status_forcelist  = self.status_forcelist)
        self.adapter          = (HTTPAdapter(max_retries=self.retry))
        self.search_url       = 'https://www.nseindia.com/api/search/autocomplete?q={}'
        self.get_details      = 'https://www.nseindia.com/api/quote-equity?symbol={}'
    
    def identifier_finder(self):
        name = self.identifier.replace(' ', '')
        session = requests.Session()
        session.mount('https://',
                      self.adapter)
        try:
            session.get('https://www.nseindia.com/',
                        headers = self.head)
            search_results = session.get(url     = self.search_url.format(name),
                                         headers = self.head)
            search_result  = search_results.json()['symbols'][0]['symbol']
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        except (IndexError, KeyError) as e:
            raise ValueError("Error: Symbol not found or invalid response from server. Please try again.",e) from None
        try:
            company_details = session.get(url     = self.get_details.format(search_result),
                                          headers = self.head)
            identifier = company_details.json()['info']['identifier']
            return identifier
        except KeyError as e:
            raise ValueError("Error: Unable to retrieve company identifier from server response.\nPlease try again with valid stock name",e) from None
        finally:
            session.close()
    
    def symbol_finder(self):
        company_name   = self.identifier.replace(' ', '')
        session        = requests.Session()
        session.mount('https://',
                      self.adapter)
        try:
            session.get('https://www.nseindia.com/',
                        headers = self.head)
            search_results = session.get(url     = self.search_url.format(company_name),
                                         headers = self.head)
            search_result  = search_results.json()['symbols'][0]['symbol']
            return str(search_result)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        except (IndexError, KeyError) as e:
            raise ValueError("Error: Symbol not found or invalid response from server. Please try again.") from None
        finally:
            session.close()
    
    def historical_ohlc(self,
                        from_date:str = (datetime.today().date() 
                                         - timedelta(days=365)).strftime("%d-%m-%Y"),
                        to_date:str   =  datetime.today().date().strftime("%d-%m-%Y")
                       )-> pd.DataFrame:
        """This function scraps historical stock data from NSE. Maximum historical data will be one year.

        Args:
            from_date ("DD-MM-YYYY", optional): Starting date in "DD-MM-YYYY" format. Defaults to today's date.
            to_date ("DD-MM-YYYY", optional): Ending date in "DD-MM-YYYY" format. Defaults to exact one year.

        Returns:
            pd.DataFrame: Daily candlestick data.
        """
        try:
            from_date = parser.parse(from_date,
                                     dayfirst= True)
            to_date   = parser.parse(to_date,
                                     dayfirst= True)
        except Exception as e:
            raise ValueError("Error: Invalid date format. Please use 'DD-MM-YYYY'.",e)
        if not (from_date <= to_date):
            raise ValueError("Error: Invalid date range. Starting date (from_date) should be earlier than ending date (to_date).")
        from_date = from_date.strftime('%d-%m-%Y')
        to_date   = to_date.strftime('%d-%m-%Y')
        company        = self.symbol_finder()
        session        = requests.Session()
        session.mount('https://',
                      self.adapter)
        try:
            session.get("https://www.nseindia.com",
                        headers = self.head)
            session.get("https://www.nseindia.com/get-quotes/equity?symbol=" 
                        + company, 
                        headers = self.head)
            session.get("https://www.nseindia.com/api/historical/cm/equity?symbol="
                        +company,
                        headers = self.head)
            url     = ("https://www.nseindia.com/api/historical/cm/equity?symbol=" 
                       + company 
                       + "&series=[%22EQ%22]&from=" 
                       + from_date 
                       + "&to=" 
                       + to_date 
                       + "&csv=true")
            webdata = session.get(url     = url,
                                  headers = self.head)
            company_historical_dataframe         = pd.read_csv(StringIO(webdata.text[3:]))
            company_historical_dataframe.columns = [str(x).lower().replace(' ','') for x in company_historical_dataframe.columns]
            company_historical_dataframe['date'] = pd.to_datetime(company_historical_dataframe['date'],
                                                                  format   = self.date_format)
            company_historical_dataframe[['volume', 'value','nooftrades']] = company_historical_dataframe[['volume',
                                                                                                           'value',
                                                                                                           'nooftrades']
                                                                                                          ].apply(
                                                                                                                    lambda x: pd.to_numeric(x.str.replace(',', '')
                                                                                                                                            )
                                                                                                                )
            company_historical_dataframe.loc[:,'symbol'] = company                                                                                  
            return company_historical_dataframe
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        finally:
            session.close()
    
    def intraday_ohlc(self,
                      tick:bool = False,
                      candlestick: int = 1) -> pd.DataFrame:
        """This function scrapes current date's listed companies spot data for the given stock name.

        Args:
            tick (bool, optional): If True returns per second tick price data . Defaults to False.
            candlestick (int, optional): Candle period in Minutes . Defaults to 1 Minute.

        Returns:
            pd.DataFrame: Intra Day stock data
        """
        stock_name = self.identifier_finder()
        session = requests.Session()
        session.mount('https://', self.adapter)
        try:
            session.get("https://www.nseindia.com",
                        headers=self.head)
            company_spot_data = pd.DataFrame(session.get(f"https://www.nseindia.com/api/chart-databyindex?index={str.upper(stock_name)}",
                                                         headers= self.head).json()['grapthData'])
            session.close()
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        company_spot_data.rename({0:"timestamp",1:"ltp"},
                                 axis    = 1,
                                 inplace = True)
        company_spot_data['timestamp'] = pd.to_datetime(company_spot_data['timestamp'],
                                                        unit='ms',
                                                        origin='unix')
        if tick:
            company_spot_data.loc[:,'symbol'] = stock_name.replace('EQN','')
            return company_spot_data
        else:
            company_spot_data = company_spot_data.set_index(company_spot_data['timestamp'])
            company_spot_data = company_spot_data[['ltp']]
            company_spot_data = company_spot_data['ltp'].resample(f'{candlestick}Min').ohlc()
            company_spot_data.loc[:,'symbol'] = stock_name.replace('EQN','')
            return company_spot_data.reset_index()
        
    def trade_reports(self,
                      from_date:str = (datetime.today().date() 
                                      - timedelta(days=100)).strftime("%d-%m-%Y"),
                      to_date:str   =  datetime.today().date().strftime("%d-%m-%Y")) -> pd.DataFrame:
        """This function scrapes the Security-wise Price volume & Deliverable position data from NSE website.

        Args:
            from_date (str, optional): Starting date in "DD-MM-YYY" format. Defaults to today's date.
            to_date (str, optional): Ending date in "DD-MM-YYY" format. Defaults to exact one year.

        Returns:
            pd.DataFrame
        """
        try:
            from_date = parser.parse(from_date,
                                     dayfirst= True)
            to_date   = parser.parse(to_date,
                                     dayfirst= True)
        except Exception as e:
            raise ValueError("Error: Invalid date format. Please use 'DD-MM-YYYY'.",e)
        if not (from_date <= to_date):
            raise ValueError("Error: Invalid date range. Starting date (from_date) should be earlier than ending date (to_date).")
        from_date    = from_date.strftime('%d-%m-%Y')
        to_date      = to_date.strftime('%d-%m-%Y')
        stock_symbol = self.symbol_finder()
        session      = requests.Session()
        session.mount('https://',
                      self.adapter)
        try:
            session.get("https://www.nseindia.com",
                        headers = self.head)
            session.get("https://www.nseindia.com/all-reports", 
                        headers = self.head)
            session.get("https://www.nseindia.com/report-detail/eq_security",
                        headers = self.head)
            url = f"https://www.nseindia.com/api/historical/securityArchives?from={from_date}&to={to_date}&symbol={stock_symbol}&dataType=priceVolumeDeliverable&series=EQ"
            res = session.get(url     = url,
                              headers = self.head).json()
            res = pd.DataFrame(res['data'])
            res.rename(columns= {'CH_SYMBOL':'symbol',
                                 'CH_TIMESTAMP':'date',
                                 'COP_DELIV_QTY':'deliverable_qty',
                                 'COP_DELIV_PERC': '%dly_qt_to_traded_qty',
                                 'CH_OPENING_PRICE':'open',
                                 'CH_TRADE_HIGH_PRICE':'high',
                                 'CH_TRADE_LOW_PRICE': 'low',
                                 'CH_CLOSING_PRICE': 'close',
                                 'CH_LAST_TRADED_PRICE':'ltp',
                                 'CH_PREVIOUS_CLS_PRICE':'prev_close',
                                 'CH_52WEEK_HIGH_PRICE':'52week_high',
                                 'CH_52WEEK_LOW_PRICE':'52week_low',
                                 'CH_TOT_TRADED_QTY':'total_traded_qty',
                                 'CH_TOT_TRADED_VAL':'turnover',
                                 'CH_TOTAL_TRADES':'total_trades',
                                 'VWAP':'vwap'},inplace= True)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        finally:
            session.close()
        return res[['symbol',
                    'date',
                    'deliverable_qty',
                    '%dly_qt_to_traded_qty',
                    'open',
                    'high',
                    'low',
                    'close',
                    'ltp',
                    'prev_close',
                    '52week_high',
                    '52week_low',
                    'total_traded_qty',
                    'turnover',
                    'total_trades',
                    'vwap']]
    
    def bulk_deals(self,from_date:str = (datetime.today().date() 
                                      - timedelta(days=100)).strftime("%d-%m-%Y"),
                        to_date:str   =  datetime.today().date().strftime("%d-%m-%Y")
                  ) -> pd.DataFrame:
        """This fucntion scraps the bulk deal/block deal data from NSE website.

        Args:
            from_date (str, optional): Starting date in "DD-MM-YYY" format. Defaults to today's date.
            to_date (str, optional): Ending date in "DD-MM-YYY" format. Defaults to exact one year.

        Returns:
            pd.DataFrame
        """
        try:
            from_date = parser.parse(from_date,
                                     dayfirst= True)
            to_date   = parser.parse(to_date,
                                     dayfirst= True)
        except Exception as e:
            raise ValueError("Error: Invalid date format. Please use 'DD-MM-YYYY'.",e)
        if not (from_date <= to_date):
            raise ValueError("Error: Invalid date range. Starting date (from_date) should be earlier than ending date (to_date).")
        from_date    = from_date.strftime('%d-%m-%Y')
        to_date      = to_date.strftime('%d-%m-%Y')
        stock_symbol = self.symbol_finder()
        session      = requests.Session()
        session.mount('https://',
                      self.adapter)
        try:
            session.get("https://www.nseindia.com",
                        headers = self.head)
            session.get("https://www.nseindia.com/all-reports", 
                        headers = self.head)
            session.get("https://www.nseindia.com/report-detail/display-bulk-and-block-deals",
                        headers = self.head)
            url = f"https://www.nseindia.com/api/historical/bulk-deals?symbol={stock_symbol}&from={from_date}&to={to_date}"
            res = session.get(url     = url,
                              headers = self.head).json()
            res = pd.DataFrame(res['data'])
            res.rename(columns= {'BD_DT_DATE':'date',
                                       'BD_SYMBOL':'symbol',
                                       'BD_SCRIP_NAME':'security_name',
                                       'BD_CLIENT_NAME':'client_name',
                                       'BD_BUY_SELL':'buy/sell',
                                       'BD_QTY_TRD':'quantity_traded',
                                       'BD_TP_WATP':'traded_price',
                                       'BD_REMARKS':'remarks'
                                       }, inplace= True)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        finally:
            session.close()
        res['date'] = pd.to_datetime(res['date'],
                                     format   = self.date_format)
        return res[['date',
                    'symbol',
                    'security_name',
                    'client_name',
                    'buy/sell',
                    'quantity_traded',
                    'traded_price',
                    'remarks']]
    
    def announcements(self,
                      from_date:str = (datetime.today().date() 
                                      - timedelta(days=100)).strftime("%d-%m-%Y"),
                      to_date:str   =  datetime.today().date().strftime("%d-%m-%Y")
                     ) -> pd.DataFrame:
        """This function scraps the announcements from the NSE website.
        
        Args:
            from_date (str, optional): Starting date in "DD-MM-YYY" format. Defaults to today's date.
            to_date (str, optional): Ending date in "DD-MM-YYY" format. Defaults to exact one year.
            
        Returns:
            pd.DataFrame: _description_
        """
        try:
            from_date = parser.parse(from_date,
                                     dayfirst= True)
            to_date   = parser.parse(to_date,
                                     dayfirst= True)
        except Exception as e:
            raise ValueError("Error: Invalid date format. Please use 'DD-MM-YYYY'.",e)
        if not (from_date <= to_date):
            raise ValueError("Error: Invalid date range. Starting date (from_date) should be earlier than ending date (to_date).")
        from_date    = from_date.strftime('%d-%m-%Y')
        to_date      = to_date.strftime('%d-%m-%Y')
        stock_symbol = self.symbol_finder()
        session      = requests.Session()
        session.mount('https://',
                      self.adapter)
        try:
            session.get("https://www.nseindia.com",
                        headers = self.head)
            session.get("https://www.nseindia.com/all-reports", 
                        headers = self.head)
            session.get("https://www.nseindia.com/report-detail/display-bulk-and-block-deals",
                        headers = self.head)
            url_ = f"https://www.nseindia.com/api/corporate-announcements?index=equities&from_date={from_date}&to_date={to_date}&symbol={stock_symbol}"
            res_ = session.get(url     = url_,
                              headers = self.head).json()
            res_ = pd.DataFrame(res_)
            print(res_.columns)
            res_.rename(columns={'sort_date':'timestamp',
                        'desc':'subject',
                        'sm_name':'company_name',
                        'sm_isin':'isin',
                        'smIndustry':'industry',
                        'attchmntText':'details',
                        'attchmntFile':'attachment',
                        }, inplace= True)
            print(res_.columns)
            return res_[['symbol',
                        'timestamp',
                        'subject',
                        'company_name',
                        'isin',
                        'industry',
                        'details',
                        'attachment']]
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        finally:
            session.close()
    
        
        
        
        
if __name__ == '__main__':
    symb = Stock('ushamart')
    df = symb.announcements('Dec 14, 2025', '25-Oct-2024')
    print(df)
    # df.to_csv("/home/ujjwal/Desktop/ushamartin_trade_report.csv",index= None)