from main import *

def get_stock_symbols(stock):
    
    url="https://pkgstore.datahub.io/core/nasdaq-listings/nasdaq-listed_csv/data/7665719fb51081ba0bd834fde71ce822/nasdaq-listed_csv.csv"
    s = requests.get(url).content
    companies = pd.read_csv(io.StringIO(s.decode('utf-8')))
    Symbols = companies['Symbol'].tolist()
    
    return Symbols

def get_stock(symbol, start, end):
    
    yf.pdr_override() 
    data = pdr.get_data_yahoo(symbol, start=start, end=end)

    return data

def clean_data(data):
    del data['Low']
    del data['Adj Close']
    del data['Volume']
   
    return data

